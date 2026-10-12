# 📈 课程学习与同步进度

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
| **Ch01_Sec11** | **Chapter_1_Section_1.1** | 2026-10-12 | 🟢 已完成 | [阅读讲义](/chapter_01/Ch01_Sec11_Chapter_1_Section_1.1) | [下载 PDF](/pdf/Ch01_Sec11_Chapter_1_Section_1.1.pdf) |

---

## ⚙️ 运维与同步指令

本地开发者可使用以下命令随时进行全量或增量同步：

```bash
# 执行一次增量同步检查并推送到 GitHub
python scripts/sync_course.py

# 启动本地实时预览服务器
npm run docs:dev

# 查看同步历史日志
type logs\sync.log
```
