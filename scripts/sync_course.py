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

def clean_latex_markdown(content):
    """
    Clean artifacts produced by Google Docs export to ensure
    perfect rendering with MathJax3 and VitePress.
    """
    # 1. Fix escaped underscores inside equations: $$... \_ ...$$ -> _
    def unescape_math_blocks(match):
        block = match.group(0)
        # Unescape underscores and asterisks in math
        block = block.replace(r"\_", "_").replace(r"\*", "*")
        return block

    # Match block equations $$...$$
    content = re.sub(r"\$\$(.*?)\$\$", unescape_math_blocks, content, flags=re.DOTALL)
    # Match inline equations $...$
    content = re.sub(r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)", unescape_math_blocks, content)

    # 2. Fix broken non-breaking spaces
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
    cmd_md = ["gdocs", "readonly", "export", doc_id, "--format", "md", "--output", str(temp_md)]
    res_md = subprocess.run(cmd_md, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res_md.returncode != 0:
        logger.warning(f"gdocs CLI md export failed: {res_md.stderr.strip()}")
        return False, None, None

    # Export PDF if requested
    export_pdf = config.get("pdf", {}).get("export_pdf", True)
    if export_pdf:
        cmd_pdf = ["gdocs", "readonly", "export", doc_id, "--format", "pdf", "--output", str(temp_pdf)]
        subprocess.run(cmd_pdf, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

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

def run_sync():
    """Main synchronization workflow."""
    logger.info("=== Starting Atmospheric Physics Study Sync ===")
    config = load_config()

    synced_items = []

    # Check local sync folder mode (if user uses Google Drive desktop client)
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

    # Check if a specific document is queued or known
    # E.g. baseline document Ch01_Sec02
    baseline_id = "1CxpOg81Hg58HKBeu8BNTwGQDPvAosu8ZfbTexmr7l9w"
    progress = load_progress()
    if baseline_id not in progress.get("documents", {}):
        # Attempt CLI pull
        success, md_file, pdf_file = sync_from_gdocs_cli(baseline_id, config)
        if success and md_file:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            name = process_and_save_lecture(content, doc_id=baseline_id, source_pdf=pdf_file)
            synced_items.append(name)

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Atmospheric Physics Sync Tool")
    parser.add_argument("--doc-id", help="Manually sync a specific Google Doc ID")
    parser.add_argument("--file", help="Manually ingest a local markdown file")
    args = parser.parse_args()

    config = load_config()

    if args.file:
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
