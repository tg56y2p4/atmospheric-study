# 南京信息工程大学《大气物理学》精讲讲义与自动化同步知识库

> **教材基准**：银燕等编著《大气物理学》（气象出版社）  
> **核心特色**：全公式族谱推导 · 微观与宏观物理机制深挖 · 典型例题与期末习题精讲  
> **技术架构**：“云端学术大脑（Gemini Spark）+ 云端数据中枢（Google Drive/Docs）+ 本地执行引擎（Antigravity）+ GitHub Pages”

---

## 🏛️ 整体协同架构

```
┌─────────────────────────────────┐
│     Gemini Spark (云端沙箱)     │
│  1. 依银燕教材推进每日精讲章节   │
│  2. 全公式族谱推导与 LaTeX 排版  │
│  3. 写入 Google Docs            │
└────────────────┬────────────────┘
                 │ 自动创建 / 更新文档
                 ▼
┌─────────────────────────────────┐
│     Google Drive (云端数据中枢) │
│  目录: Atmospheric_Physics_Course │
│  • Ch01_Sec02_大气的基础知识.gdoc │
│  • progress_index.json          │
└────────────────┬────────────────┘
                 │ 每日定时检测并拉取
                 ▼
┌─────────────────────────────────┐
│    Antigravity (本地执行引擎)    │
│  1. 检测 Google Drive/Docs 增量  │
│  2. 格式规范化、LaTeX 修复与归档 │
│  3. 导出本地 Markdown 与 PDF    │
│  4. 自动 Git Commit & Git Push   │
└────────────────┬────────────────┘
                 │ 自动推送至 GitHub
                 ▼
┌─────────────────────────────────┐
│     GitHub & GitHub Pages       │
│  • 仓库持久化与版本历史追溯     │
│  • GitHub Actions 自动编译上线   │
└─────────────────────────────────┘
```

---

## 📁 项目目录结构

```text
d:\chuan1\
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions 自动构建与发布 Pages
├── docs/                           # 讲义 Markdown 核心库
│   ├── .vitepress/
│   │   └── config.mjs              # 静态站点配置 (MathJax3 + 动态侧边栏)
│   ├── chapter_01/                 # 第 1 章讲义
│   │   └── Ch01_Sec02_大气的基础知识.md
│   ├── index.md                    # 知识库主页与大纲
│   ├── progress.md                 # 学习进度与章节同步状态表
│   └── progress_index.json         # 结构化同步元数据索引
├── pdf/                            # 高质量 PDF 讲义归档
├── scripts/                        # 本地自动化引擎脚本
│   ├── sync_course.py              # 核心同步主程序
│   ├── git_sync.py                 # Git 自动化提交与推送模块
│   ├── run_sync.bat                # Windows 批处理入口 (供任务计划程序调用)
│   ├── run_sync.ps1                # PowerShell 脚本入口
│   └── sync_cron.sh                # Linux / WSL / macOS 调度脚本
├── logs/                           # 每日运行与异常追踪日志
│   └── sync.log
├── config.json                     # 自动化流水线配置文件
├── setup_scheduler.ps1             # Windows 计划任务一键配置工具
├── package.json                    # 前端依赖配置 (VitePress + MathJax3)
└── README.md
```

---

## 🚀 快速使用指南

### 1. 配置远程 GitHub 仓库
在本地仓库中关联你的 GitHub 仓库（若未关联）：
```powershell
git remote add origin https://github.com/<你的用户名>/<你的仓库名>.git
git push -u origin main
```
> 推送后，GitHub Actions 会根据 `.github/workflows/deploy.yml` 自动开启 GitHub Pages 网站部署。进入 GitHub 仓库的 `Settings -> Pages`，选择 Source 为 `GitHub Actions` 即可。

### 2. 运行一次同步
```powershell
# 运行主同步脚本（检测增量 -> 本地落盘 -> 格式化 -> Git 提交）
python scripts/sync_course.py

# 或使用批处理脚本
.\scripts\run_sync.bat
```

### 3. 配置 Windows 每日自动定时执行
运行项目根目录下的配置脚本，自动在 Windows 任务计划程序中注册每日上午 09:00 执行的后台任务：
```powershell
powershell -File setup_scheduler.ps1 -Time "09:00"
```
常用管理命令：
- 查看任务状态：`powershell -File setup_scheduler.ps1 -Status`
- 卸载任务：`powershell -File setup_scheduler.ps1 -Uninstall`

---

## 🌐 接入 Google Drive / Docs 的三种方式

在 `config.json` 中可灵活选择同步来源：

### 方式 1：本地 Google Drive 客户端同步（推荐，免鉴权）
1. 在本地电脑安装 Google Drive 桌面客户端；
2. 将云端 `Atmospheric_Physics_Course` 文件夹同步到本地目录（如 `G:\我的云端硬盘\Atmospheric_Physics_Course`）；
3. 在 `config.json` 中配置：
   ```json
   "google_drive": {
     "local_sync_folder": "G:\\我的云端硬盘\\Atmospheric_Physics_Course"
   }
   ```
4. 流水线会自动监控该本地目录下的所有新增章节。

### 方式 2：使用 Antigravity 内置 gdocs CLI
1. 在控制台运行登录指令（仅需一次 OAuth 授权）：
   ```powershell
   gdocs auth login
   ```
2. 直接通过文档 ID 增量同步：
   ```powershell
   python scripts/sync_course.py --doc-id <GOOGLE_DOC_ID>
   ```

### 方式 3：手动导入特定 Markdown 文件
若在本地或其他位置编写了讲义，可直接导入：
```powershell
python scripts/sync_course.py --file "路径/Ch01_Sec03_大气静力学.md"
```

---

## 📖 本地讲义网页预览

知识库内置了基于 VitePress 与 MathJax3 的学术文档系统：
```powershell
# 启动本地实时热重载预览服务器
npm run docs:dev

# 本地静态构建测试
npm run docs:build
```
启动后在浏览器访问 `http://localhost:5173` 即可沉浸式研读讲义。
