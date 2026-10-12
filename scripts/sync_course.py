#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atmospheric Physics Course Sync Pipeline
Synchronizes lecture notes from Google Drive / Docs to local docs/ and GitHub Pages.

Author: Antigravity & Gemini Spark
"""

import os
import re
import sys
import json
import shutil
import logging
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# Setup logging
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "sync.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("CourseSync")

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = ROOT_DIR / "config.json"

def load_config():
    if not CONFIG_FILE.exists():
        logger.warning(f"Config file not found at {CONFIG_FILE}, using defaults.")
        return {}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_progress():
    progress_file = ROOT_DIR / "docs" / "progress_index.json"
    if not progress_file.exists():
        return {"last_sync_time": "", "total_chapters": 0, "documents": {}}
    try:
        with open(progress_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading progress_index.json: {e}")
        return {"last_sync_time": "", "total_chapters": 0, "documents": {}}

def save_progress(data):
    progress_file = ROOT_DIR / "docs" / "progress_index.json"
    progress_file.parent.mkdir(parents=True, exist_ok=True)
    with open(progress_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info("Updated docs/progress_index.json")

def parse_frontmatter(content):
    """Extract YAML frontmatter and clean markdown content."""
    meta = {}
    body = content
    pattern = r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$"
    match = re.match(pattern, content, re.DOTALL)
    if match:
        yaml_text = match.group(1)
        body = match.group(2)
        for line in yaml_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip("\"'")
    return meta, body

def extract_metadata_from_body(body, doc_meta=None):
    """Fallback metadata extractor when Google Docs has no YAML Frontmatter."""
    meta = {}
    doc_name = doc_meta.get("name", "") if doc_meta else ""
    first_lines = "\n".join(body.splitlines()[:10])
    combined_text = doc_name + "\n" + first_lines

    # Detect chapter
    ch_match = re.search(r"第\s*(\d+)\s*章|Ch(\d+)", combined_text, re.IGNORECASE)
    if ch_match:
        meta["chapter"] = int(ch_match.group(1) or ch_match.group(2))
    else:
        meta["chapter"] = 1

    # Detect section
    sec_match = re.search(r"(\d+\.\d+)", combined_text)
    if sec_match:
        meta["section"] = sec_match.group(1)
    else:
        meta["section"] = f"{meta['chapter']}.1"

    # Detect title
    title_match = re.search(r"(?:第\s*\d+\s*章.*?·\s*\d+\.\d+\s*|Ch\d+_Sec\d+_)([\u4e00-\u9fa5\w\s]+)", combined_text)
    if title_match:
        meta["title"] = title_match.group(1).split("（")[0].strip()
    elif "大气" in doc_name:
        clean = re.sub(r"^南京信息工程大学《大气物理学》精讲讲义[_\s]*", "", doc_name)
        meta["title"] = clean.strip()
    else:
        meta["title"] = f"Chapter_{meta['chapter']}_Section_{meta['section']}"

    meta["status"] = "completed"
    meta["date"] = datetime.now().strftime("%Y-%m-%d")
    return meta

def clean_latex_markdown(content):
    """
    Clean artifacts produced by Google Docs export to ensure
    perfect rendering with MathJax3 and VitePress.
    """
    # 1. Clean HTML entity escapes
    content = content.replace(r"\&lt;\&lt;", r"\ll ").replace(r"\&gt;\&gt;", r"\gg ")
    content = content.replace(r"\&lt;", "<").replace(r"\&gt;", ">")
    content = content.replace("&lt;", "<").replace("&gt;", ">")

    # 2. Fix Google Docs unnecessary backslash escapes on markdown syntax
    content = content.replace(r"\=", "=").replace(r"\[", "[").replace(r"\]", "]")
    content = content.replace(r"\+", "+").replace(r"\-", "-")

    # 3. Fix escaped underscores inside equations: $$... \_ ...$$ -> _
    def unescape_math_blocks(match):
        block = match.group(0)
        block = block.replace(r"\_", "_").replace(r"\*", "*")
        return block

    content = re.sub(r"\$\$(.*?)\$\$", unescape_math_blocks, content, flags=re.DOTALL)
    content = re.sub(r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)", unescape_math_blocks, content)

    # 4. Fix non-breaking spaces
    content = content.replace("\u00a0", " ")

    return content

def update_progress_page():
    """Regenerate docs/progress.md table from progress_index.json."""
    data = load_progress()
    progress_md_path = ROOT_DIR / "docs" / "progress.md"
    
    docs = data.get("documents", {})
    sorted_docs = sorted(docs.values(), key=lambda x: (x.get("chapter", 0), str(x.get("section", ""))))
    
    table_rows = []
    for d in sorted_docs:
        title = d.get("title", "")
        clean_title = re.sub(r"^Ch\d+_Sec\d+_", "", title)
        sec = d.get("section", "")
        ch = d.get("chapter", 1)
        ch_tag = f"Ch{ch:02d}_Sec{sec.replace('.', '') if isinstance(sec, str) else sec}"
        date = d.get("last_synced", "")[:10]
        status = "🟢 已完成" if d.get("status") == "completed" else "🟡 同步中"
        fpath = d.get("file_path", "")
        if fpath:
            clean_fpath = re.sub(r"^docs/", "", fpath)
            clean_fpath = re.sub(r"\.md$", "", clean_fpath)
            rel_link = "/" + clean_fpath
        else:
            rel_link = ""
        pdf_link = "/" + d.get("pdf_path", "") if d.get("pdf_path") else ""
        
        row = f"| **{ch_tag}** | **{clean_title}** | {date} | {status} | [阅读讲义]({rel_link}) | [下载 PDF]({pdf_link}) |"
        table_rows.append(row)
        
    table_content = "\n".join(table_rows) if table_rows else "| 暂无已同步章节 | - | - | - | - | - |"
    
    doc_text = f"""# 📈 课程学习与同步进度

本页面由本地同步引擎 `Antigravity` 配合 `progress_index.json` 自动更新维护。

## 🎯 当前推进状态

- **教材基准**：银燕等编著《大气物理学》（气象出版社）
- **同步工作流状态**：
  - 🔄 **云端源库**：Google Drive (`Atmospheric_Physics_Course`)
  - 📥 **本地落盘**：`docs/chapter_XX/` + `pdf/`
  - 🚀 **远程仓库**：GitHub Pages 自动部署

---

## 📑 章节清单与流水线索引

| 章节 | 标题 | 完成日期 | 状态 | 在线阅读 | PDF 下载 |
| :--- | :--- | :--- | :--- | :--- | :--- |
{table_content}

---

## ⚙️ 运维与同步指令

本地开发者可使用以下命令随时进行全量或增量同步：

```bash
# 执行一次增量同步检查并推送到 GitHub
python scripts/sync_course.py

# 启动本地实时预览服务器
npm run docs:dev

# 查看同步历史日志
type logs\\sync.log
```
"""
    with open(progress_md_path, "w", encoding="utf-8") as f:
        f.write(doc_text)
    logger.info("Refreshed docs/progress.md")

def sync_from_gdocs_cli(doc_id, config):
    """Fetch doc via gdocs CLI tool."""
    logger.info(f"Attempting to fetch Google Doc {doc_id} via gdocs CLI...")
    temp_dir = ROOT_DIR / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    temp_md = temp_dir / f"{doc_id}.md"
    temp_pdf = temp_dir / f"{doc_id}.pdf"

    # Export Markdown
    cmd_md = f'gdocs readonly export {doc_id} --format md --output "{temp_md}"'
    res_md = subprocess.run(cmd_md, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, encoding="utf-8", errors="replace")
    if res_md.returncode != 0:
        logger.warning(f"gdocs CLI md export failed: {res_md.stderr.strip()}")
        return False, None, None

    # Export PDF if requested
    export_pdf = config.get("pdf", {}).get("export_pdf", True)
    if export_pdf:
        cmd_pdf = f'gdocs readonly export {doc_id} --format pdf --output "{temp_pdf}"'
        subprocess.run(cmd_pdf, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, encoding="utf-8", errors="replace")

    return True, temp_md, temp_pdf if temp_pdf.exists() else None

def process_and_save_lecture(markdown_content, doc_id=None, source_pdf=None):
    """Process frontmatter, normalize LaTeX, and save to docs/chapter_XX/."""
    meta, body = parse_frontmatter(markdown_content)
    clean_body = clean_latex_markdown(body)

    chapter = int(meta.get("chapter", 1))
    section = meta.get("section", "1.1")
    title = meta.get("title", f"Chapter_{chapter}_Section_{section}")
    
    # Standard file name
    clean_title = re.sub(r"[\\/*?:\"<>|]", "_", title).strip()
    sec_tag = str(section).replace(".", "")
    filename = f"Ch{chapter:02d}_Sec{sec_tag}_{clean_title}.md"

    # Chapter directory
    chapter_dir = ROOT_DIR / "docs" / f"chapter_{chapter:02d}"
    chapter_dir.mkdir(parents=True, exist_ok=True)
    target_md = chapter_dir / filename

    # Reconstruct clean markdown with frontmatter
    final_content = f"""---
chapter: {chapter}
section: {section}
title: {clean_title}
date: {meta.get('date', datetime.now().strftime('%Y-%m-%d'))}
status: {meta.get('status', 'completed')}
source_doc_id: {doc_id or meta.get('source_doc_id', '')}
---

{clean_body.strip()}
"""

    with open(target_md, "w", encoding="utf-8") as f:
        f.write(final_content)
    logger.info(f"Saved processed lecture note to {target_md}")

    # --- Pre-Publish Integrity Verification ---
    from verify_lecture import verify_lecture_file
    report = verify_lecture_file(target_md)
    if not report.is_valid:
        logger.error(f"[QUALITY ALERT] Integrity check FAILED for {filename}!")
        for err in report.errors:
            logger.error(f"  * [ERROR] {err}")
        quarantine = LOG_DIR / f"corrupted_{filename}"
        shutil.copy2(target_md, quarantine)
        logger.error(f"Quarantined suspicious file to {quarantine}. Aborting commit to prevent live site corruption.")
        return None

    if report.warnings:
        for w in report.warnings:
            logger.warning(f"[Quality Warning] {filename}: {w}")

    logger.info(
        f"[Quality OK] {filename} passed all checks: "
        f"{report.stats.get('char_count', 0)} chars, "
        f"{report.stats.get('block_equations_count', 0)} block equations, "
        f"{report.stats.get('inline_equations_count', 0)} inline equations, "
        f"{report.stats.get('table_count', 0)} tables."
    )

    # Copy PDF if exists
    pdf_rel_path = ""
    if source_pdf and Path(source_pdf).exists():
        pdf_dir = ROOT_DIR / "pdf"
        pdf_dir.mkdir(parents=True, exist_ok=True)
        target_pdf = pdf_dir / f"Ch{chapter:02d}_Sec{sec_tag}_{clean_title}.pdf"
        shutil.copy2(source_pdf, target_pdf)
        pdf_rel_path = f"pdf/{target_pdf.name}"
        logger.info(f"Saved lecture PDF to {target_pdf}")

    # Update progress index
    progress = load_progress()
    key = doc_id or filename
    progress["documents"][key] = {
        "title": f"Ch{chapter:02d}_Sec{sec_tag}_{clean_title}",
        "chapter": chapter,
        "section": section,
        "file_path": f"docs/chapter_{chapter:02d}/{filename}",
        "pdf_path": pdf_rel_path,
        "status": meta.get("status", "completed"),
        "last_synced": datetime.now().isoformat()
    }
    progress["last_sync_time"] = datetime.now().isoformat()
    progress["total_chapters"] = len(progress["documents"])
    save_progress(progress)
    update_progress_page()

    return filename

def discover_cloud_google_docs():
    """
    Search Google Drive for lecture notes created by Gemini Spark.
    Checks recent files and query keywords.
    """
    found_docs = {}

    # 1. Search recent files on Google Drive
    try:
        cmd = "gdrive readonly recent --max 30 --json"
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, encoding="utf-8", errors="replace")
        if res.returncode == 0 and res.stdout.strip():
            items = json.loads(res.stdout)
            for item in items:
                if item.get("mimeType") == "application/vnd.google-apps.document":
                    name = item.get("name", "")
                    if any(k in name for k in ["大气物理学", "大气", "Atmospheric", "Ch0", "Ch1", "讲义"]):
                        doc_id = item.get("id")
                        if doc_id:
                            found_docs[doc_id] = item
    except Exception as e:
        logger.warning(f"Error checking recent files on Google Drive: {e}")

    # 2. Search specific queries
    for kw in ["大气物理学", "Atmospheric_Physics_Course"]:
        try:
            cmd = f'gdrive readonly search --name-contains "{kw}" --json'
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, encoding="utf-8", errors="replace")
            if res.returncode == 0 and res.stdout.strip():
                items = json.loads(res.stdout)
                for item in items:
                    if item.get("mimeType") == "application/vnd.google-apps.document":
                        doc_id = item.get("id")
                        if doc_id and doc_id not in found_docs:
                            found_docs[doc_id] = item
        except Exception as e:
            logger.warning(f"Error searching Google Drive for '{kw}': {e}")

    return list(found_docs.values())

def run_sync():
    """Main synchronization workflow."""
    logger.info("=== Starting Atmospheric Physics Study Sync ===")
    config = load_config()

    synced_items = []

    # 1. Check local sync folder mode (if user uses Google Drive desktop client)
    local_drive = config.get("google_drive", {}).get("local_sync_folder", "")
    if local_drive and os.path.exists(local_drive):
        logger.info(f"Scanning local Google Drive sync folder: {local_drive}")
        for root, _, files in os.walk(local_drive):
            for file in files:
                if file.endswith((".md", ".txt")) and file.startswith("Ch"):
                    file_path = os.path.join(root, file)
                    logger.info(f"Found lecture file: {file_path}")
                    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                    name = process_and_save_lecture(content)
                    synced_items.append(name)

    # 2. Automatic Cloud Discovery from Google Docs / Google Drive
    cloud_docs = discover_cloud_google_docs()
    logger.info(f"Discovered {len(cloud_docs)} lecture document(s) on Google Drive.")
    progress = load_progress()

    for cdoc in cloud_docs:
        doc_id = cdoc["id"]
        doc_name = cdoc.get("name", "")
        mod_time = cdoc.get("modifiedTime", "")

        # Check if already synced and up to date
        existing = progress.get("documents", {}).get(doc_id)
        if existing and existing.get("last_modified") == mod_time:
            logger.info(f"Document '{doc_name}' ({doc_id}) is up to date. Skipping.")
            continue

        logger.info(f"Pulling new or updated Google Doc from cloud: '{doc_name}' ({doc_id})...")
        success, md_file, pdf_file = sync_from_gdocs_cli(doc_id, config)
        if success and md_file:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            name = process_and_save_lecture(content, doc_id=doc_id, source_pdf=pdf_file)
            if name:
                synced_items.append(name)
                progress = load_progress()
                if doc_id in progress.get("documents", {}):
                    progress["documents"][doc_id]["last_modified"] = mod_time
                    save_progress(progress)

    # Pre-publish Quality Gate: Audit all lecture notes
    from verify_lecture import verify_lecture_file
    all_lectures = list((ROOT_DIR / "docs").glob("chapter_*/*.md"))
    has_critical_failure = False
    for lec in all_lectures:
        rep = verify_lecture_file(lec)
        if not rep.is_valid:
            has_critical_failure = True
            logger.error(f"[Quality Gate] Lecture {lec.name} failed verification! Refusing to push.")
            for err in rep.errors:
                logger.error(f"  * {err}")

    if has_critical_failure:
        logger.error("Quality Gate: Aborting Git push because one or more files failed integrity check.")
        return

    # Git Sync Step
    if config.get("git", {}).get("auto_commit", True):
        from git_sync import git_commit_and_push, has_changes
        if has_changes(ROOT_DIR):
            commit_title = synced_items[0] if synced_items else "latest lecture updates"
            msg = config.get("git", {}).get("commit_msg_template", "feat(study): auto-sync {title}").format(title=commit_title)
            branch = config.get("git", {}).get("branch", "main")
            remote = config.get("git", {}).get("remote", "origin")
            git_commit_and_push(ROOT_DIR, commit_msg=msg, branch=branch, remote=remote)
        else:
            logger.info("No git changes detected. Skipping commit.")

    logger.info("=== Sync finished successfully ===")

def audit_all_lectures():
    """Audit all existing lectures in docs/chapter_*."""
    from verify_lecture import verify_lecture_file
    all_lectures = list((ROOT_DIR / "docs").glob("chapter_*/*.md"))
    print("=" * 60)
    print(f" 全量讲义内容完整性与质量体检 (共 {len(all_lectures)} 篇)")
    print("=" * 60)
    all_passed = True
    for lec in sorted(all_lectures):
        rep = verify_lecture_file(lec)
        s = rep.summary()
        status_tag = "[PASS]" if s["is_valid"] else "[FAIL]"
        print(f"\n{status_tag} {lec.name}")
        print(f"  - 字符/行数: {s['stats'].get('char_count', 0)} 字 / {s['stats'].get('line_count', 0)} 行")
        print(f"  - 块级公式 ($$): {s['stats'].get('block_equations_count', 0)} | 行内公式 ($): {s['stats'].get('inline_equations_count', 0)}")
        print(f"  - 表格: {s['stats'].get('table_count', 0)} 个 | 结构: H1={s['stats'].get('h1_count', 0)}, H2={s['stats'].get('h2_count', 0)}, H3={s['stats'].get('h3_count', 0)}")
        if s["errors"]:
            all_passed = False
            for err in s["errors"]:
                print(f"  * 错误: {err}")
        if s["warnings"]:
            for w in s["warnings"]:
                print(f"  * 警告: {w}")
    print("\n" + "=" * 60)
    print("体检完成: " + ("全量讲义健康通过！" if all_passed else "存在质检不合格文件，已阻断发布！"))
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Atmospheric Physics Sync Tool")
    parser.add_argument("--doc-id", help="Manually sync a specific Google Doc ID")
    parser.add_argument("--file", help="Manually ingest a local markdown file")
    parser.add_argument("--check", action="store_true", help="Audit all local lecture notes")
    args = parser.parse_args()

    config = load_config()

    if args.check:
        audit_all_lectures()
    elif args.file:
        logger.info(f"Manually ingesting file: {args.file}")
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
        name = process_and_save_lecture(content)
        if config.get("git", {}).get("auto_commit", True):
            from git_sync import git_commit_and_push
            git_commit_and_push(ROOT_DIR, commit_msg=f"feat(study): auto-sync {name}")
    elif args.doc_id:
        logger.info(f"Manually syncing Google Doc ID: {args.doc_id}")
        success, md_file, pdf_file = sync_from_gdocs_cli(args.doc_id, config)
        if success and md_file:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            name = process_and_save_lecture(content, doc_id=args.doc_id, source_pdf=pdf_file)
            if config.get("git", {}).get("auto_commit", True):
                from git_sync import git_commit_and_push
                git_commit_and_push(ROOT_DIR, commit_msg=f"feat(study): auto-sync {name}")
    else:
        run_sync()
