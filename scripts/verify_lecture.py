#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lecture Note Quality & Integrity Verifier
Automatically inspects lecture markdown files for content loss, broken formulas,
truncated sections, and formatting degradation before daily publishing.

Author: Antigravity & Gemini Spark
"""

import re
import sys
import json
import logging
from pathlib import Path

# Force UTF-8 on Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

logger = logging.getLogger("LectureVerifier")

class LectureIntegrityReport:
    def __init__(self, file_path):
        self.file_path = str(file_path)
        self.is_valid = True
        self.errors = []
        self.warnings = []
        self.stats = {}

    def add_error(self, msg):
        self.is_valid = False
        self.errors.append(msg)

    def add_warning(self, msg):
        self.warnings.append(msg)

    def summary(self):
        status = "PASSED" if self.is_valid and not self.warnings else ("PASSED WITH WARNINGS" if self.is_valid else "FAILED")
        return {
            "file": self.file_path,
            "status": status,
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "stats": self.stats
        }

def verify_frontmatter(content, report):
    pattern = r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n"
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        report.add_error("缺失 YAML Frontmatter 元数据块 (必须以 --- 开头并闭合)")
        return {}

    yaml_text = match.group(1)
    meta = {}
    for line in yaml_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip("\"'")

    required_fields = ["chapter", "section", "title", "status"]
    missing = [f for f in required_fields if f not in meta]
    if missing:
        report.add_error(f"Frontmatter 缺失必要字段: {', '.join(missing)}")

    if "chapter" in meta:
        try:
            int(meta["chapter"])
        except ValueError:
            report.add_error(f"Frontmatter 'chapter' 字段必须为整数，当前为: {meta['chapter']}")

    report.stats["frontmatter"] = meta
    return meta

def verify_latex_math(content, report):
    r"""
    Check LaTeX equation integrity:
    1. Paired $$ and $
    2. Check for mangled escape sequences (e.g. \_, \*, \$, unescaped brackets)
    3. Balanced braces inside equations
    """
    # 1. Check block equations $$...$$
    block_delimiter_count = content.count("$$")
    if block_delimiter_count % 2 != 0:
        report.add_error(f"块级 LaTeX 符号 '$$' 数量不匹配 (共 {block_delimiter_count} 个，必须成对出现)")

    # Find all $$...$$ blocks
    block_equations = re.findall(r"\$\$(.*?)\$\$", content, re.DOTALL)
    report.stats["block_equations_count"] = len(block_equations)

    for i, eq in enumerate(block_equations, 1):
        if not eq.strip():
            report.add_warning(f"发现空的块级公式块 ($$) 第 {i} 处")
        # Check braces balance
        open_braces = eq.count("{")
        close_braces = eq.count("}")
        if open_braces != close_braces:
            report.add_error(f"第 {i} 个块级公式大括号数量不平衡: 开括号 '{open_braces}' vs 闭括号 '{close_braces}'\n内容片段: {eq[:60]}...")
        # Check for escaped underscores inside math
        if r"\_" in eq:
            report.add_warning(f"第 {i} 个块级公式中含有被转义的下划线 '\\_'，可能影响下标解析")

    # 2. Check inline equations $...$ (excluding $$)
    # Strip out block equations first
    content_no_blocks = re.sub(r"\$\$.*?\$\$", "", content, flags=re.DOTALL)
    # Strip out code blocks
    content_no_code = re.sub(r"```.*?```", "", content_no_blocks, flags=re.DOTALL)
    content_no_code = re.sub(r"`.*?`", "", content_no_code)

    inline_dollars = content_no_code.count("$")
    if inline_dollars % 2 != 0:
        report.add_error(f"行内 LaTeX 符号 '$' 数量不匹配 (共 {inline_dollars} 个，必须成对出现)")

    inline_equations = re.findall(r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)", content_no_code)
    report.stats["inline_equations_count"] = len(inline_equations)

    for i, eq in enumerate(inline_equations, 1):
        if not eq.strip():
            report.add_warning(f"发现空的行内公式 ($$) 第 {i} 处")
        open_b = eq.count("{")
        close_b = eq.count("}")
        if open_b != close_b:
            report.add_error(f"第 {i} 个行内公式大括号数量不平衡: 开括号 '{open_b}' vs 闭括号 '{close_b}': ${eq}$")

def verify_tables(content, report):
    """Check Markdown table structure integrity."""
    lines = content.splitlines()
    table_count = 0
    in_table = False
    col_counts = []

    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            if not in_table:
                in_table = True
                table_count += 1
                col_counts = []
            cells = [c.strip() for c in stripped[1:-1].split("|")]
            col_counts.append((idx, len(cells)))
        else:
            if in_table:
                in_table = False
                # Verify column count consistency in this table
                if col_counts:
                    expected_cols = col_counts[0][1]
                    for line_no, cols in col_counts:
                        if cols != expected_cols:
                            report.add_warning(f"第 {table_count} 个表格在第 {line_no} 行列数不一致 (首行 {expected_cols} 列，该行 {cols} 列)")

    report.stats["table_count"] = table_count

def verify_structural_content(content, report):
    """Ensure document has meaningful headings, substance, and no truncated sections."""
    lines = content.splitlines()
    
    # 1. Total character and line check
    total_chars = len(content.strip())
    total_lines = len(lines)
    report.stats["char_count"] = total_chars
    report.stats["line_count"] = total_lines

    if total_chars < 500:
        report.add_error(f"讲义内容体量过小 ({total_chars} 字符)，疑似拉取截断或空文件")
    elif total_chars < 1500:
        report.add_warning(f"讲义内容较短 ({total_chars} 字符)，请确认是否为完整章节")

    # 2. Heading analysis
    h1 = [l for l in lines if l.startswith("# ")]
    h2 = [l for l in lines if l.startswith("## ")]
    h3 = [l for l in lines if l.startswith("### ")]
    report.stats["h1_count"] = len(h1)
    report.stats["h2_count"] = len(h2)
    report.stats["h3_count"] = len(h3)

    if len(h1) == 0:
        report.add_error("缺失 1 级标题 (# 章节大标题)")
    if len(h2) < 2:
        report.add_warning(f"2 级标题数量偏少 ({len(h2)} 个)，请确认知识点是否完整展开")

    # 3. Core academic module check (Syllabus requirements)
    core_keywords = {
        "公式推导": any(kw in content for kw in ["推导", "方程", "公式", "状态方程", "克拉珀龙", "虚温"]),
        "物理机制": any(kw in content for kw in ["物理", "机制", "本质", "物理意义", "层结", "密度"]),
        "例题/习题": any(kw in content for kw in ["例题", "习题", "思考题", "考点", "计算", "证明"])
    }
    report.stats["pedagogical_modules"] = core_keywords
    for module, present in core_keywords.items():
        if not present:
            report.add_warning(f"未检测到推荐的核心学术模块: 【{module}】")

def verify_lecture_file(file_path):
    """Main verification entry point for a single lecture file."""
    path = Path(file_path).resolve()
    report = LectureIntegrityReport(path)

    if not path.exists():
        report.add_error(f"文件不存在: {path}")
        return report

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        report.add_error(f"无法读取文件 (编码或读取错误): {e}")
        return report

    verify_frontmatter(content, report)
    verify_latex_math(content, report)
    verify_tables(content, report)
    verify_structural_content(content, report)

    return report

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent.parent / "docs" / "chapter_01" / "Ch01_Sec02_大气的基础知识.md")
    rep = verify_lecture_file(target)
    summary = rep.summary()
    print("=" * 60)
    print(" [讲义内容完整性与排版质量体检报告]")
    print(f" 目标文件: {summary['file']}")
    print(f" 质检结论: {summary['status']}")
    print("=" * 60)
    print(f" - 字符统计: {summary['stats'].get('char_count', 0)} 字 / {summary['stats'].get('line_count', 0)} 行")
    print(f" - 公式统计: 块级公式 ($$) {summary['stats'].get('block_equations_count', 0)} 个 | 行内公式 ($) {summary['stats'].get('inline_equations_count', 0)} 个")
    print(f" - 章节结构: H1={summary['stats'].get('h1_count', 0)} | H2={summary['stats'].get('h2_count', 0)} | H3={summary['stats'].get('h3_count', 0)} | 表格={summary['stats'].get('table_count', 0)} 个")
    print(f" - 教学模块: {summary['stats'].get('pedagogical_modules', {})}")
    
    if summary["errors"]:
        print("\n [!] 发现严重错误 (阻断发布):")
        for err in summary["errors"]:
            print(f"   * {err}")
    else:
        print("\n [OK] 未发现语法截断或公式缺失错误！")

    if summary["warnings"]:
        print("\n [?] 发现优化建议 / 告警:")
        for w in summary["warnings"]:
            print(f"   * {w}")

    sys.exit(0 if summary["is_valid"] else 1)
