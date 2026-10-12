---
layout: home

hero:
  name: "大气物理学精讲讲义"
  text: "全公式族谱推导 · 物理机制深挖 · 习题详解"
  tagline: "基于南京信息工程大学 银燕《大气物理学》标准教材体系"
  image:
    src: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><circle cx='100' cy='100' r='80' fill='%233b82f6' opacity='0.2'/><path d='M60 110 Q100 60 140 110 T180 110' stroke='%232563eb' stroke-width='6' fill='none'/><circle cx='100' cy='100' r='8' fill='%231d4ed8'/></svg>"
    alt: Atmospheric Physics
  actions:
    - theme: brand
      text: 开始研读（第 1 章 1.2 节）
      link: /chapter_01/Ch01_Sec02_大气的基础知识
    - theme: alt
      text: 查看学习进度与流水线
      link: /progress

features:
  - icon: 📐
    title: 全公式族谱严密推导
    details: 拒绝“直接给出公式”，所有状态方程、静力学方程、压高公式、虚温定义均从热力学第一定律与流体力学守恒律完整展开推导。
  - icon: 🧠
    title: 物理机制机理深挖
    details: 结合气象学微观物理图像与宏观热力过程，深度剖析大气垂直层结、气块抬升、凝结潜热与能量转换规律。
  - icon: ⚡
    title: 双脑协同自动化流水线
    details: 云端学术大脑（Gemini Spark）输出原生 LaTeX 讲义并暂存 Google Drive，本地引擎（Antigravity）自动化拉取、测试、格式转换并推送到 GitHub Pages。
---

## 📚 课程结构总览

根据银燕《大气物理学》核心课程大纲，本精讲体系规划覆盖以下各大核心模块：

| 章节编号 | 模块名称 | 核心物理机制与推导重点 | 进度状态 |
| :--- | :--- | :--- | :--- |
| **第 1 章** | **地球大气的成分及结构** | 准均质层、理想气体状态方程推导、虚温 $T_v$ 物理意义、分压定律 | 🟢 进行中 |
| **第 2 章** | **大气静力学与热力学** | 流体静力学平衡、压高公式三种积分模型、绝热直减率 $\Gamma_d$、位温 $\theta$、静力稳定度 | 🟡 备课中 |
| **第 3 章** | **大气辐射学基础** | 普朗克定律、斯特藩-玻尔兹曼定律、吸收发射系数、大气温室效应定量推导 | ⚪ 待更新 |
| **第 4 章** | **大气水分与相变过程** | 克劳修斯-克拉珀龙方程推导、水汽参量全族谱、凝结核与凝结增长 | ⚪ 待更新 |
| **第 5 章** | **云降水微物理学** | 柯勒理论、水滴碰撞合并、暖云与冷云降水机制、冰晶繁生 | ⚪ 待更新 |
| **第 6 章** | **大气边界层与湍流扩散** | 混合长理论、理查逊数 $Ri$、莫宁-奥布霍夫相似理论、风随高度分布 | ⚪ 待更新 |

---

## 🛠️ 自动化流水线机制

本知识库采用自动同步架构：
1. **云端撰写**：Gemini Spark 按照标准 LaTeX 撰写每日新章节，存入 Google Drive 文件夹 `Atmospheric_Physics_Course`。
2. **本地抓取**：Antigravity 每日定时运行 `scripts/sync_course.py`，拉取最新 Google Docs。
3. **格式化与发布**：脚本更新 `docs/` Markdown 文件与本地 `pdf/`，执行 `git commit & push`。
4. **静态网站部署**：GitHub Actions 自动构建 VitePress 并上线到 GitHub Pages。
