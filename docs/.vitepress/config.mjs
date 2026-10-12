import { defineConfig } from 'vitepress'
import mathjax3 from 'markdown-it-mathjax3'
import fs from 'fs'
import path from 'path'

// Helper to load dynamic sidebar if available
function getDynamicSidebar() {
  const progressPath = path.resolve(__dirname, '../progress_index.json')
  if (!fs.existsSync(progressPath)) {
    return [
      {
        text: '第 1 章 行星大气与地球大气的成分及结构',
        collapsed: false,
        items: [
          { text: '1.2 大气的基础知识', link: '/chapter_01/Ch01_Sec02_大气的基础知识' }
        ]
      }
    ]
  }

  try {
    const data = JSON.parse(fs.readFileSync(progressPath, 'utf8'))
    const chapters = {}
    for (const [id, doc] of Object.entries(data.documents || {})) {
      const chNum = doc.chapter || 1
      const chKey = `第 ${chNum} 章`
      if (!chapters[chKey]) {
        chapters[chKey] = {
          text: chKey,
          collapsed: false,
          items: []
        }
      }
      const relLink = doc.file_path ? '/' + doc.file_path.replace(/^docs\//, '').replace(/\.md$/, '') : ''
      chapters[chKey].items.push({
        text: `${doc.section || ''} ${doc.title.replace(/^Ch\d+_Sec\d+_/, '')}`.trim(),
        link: relLink
      })
    }
    return Object.values(chapters)
  } catch (e) {
    return []
  }
}

export default defineConfig({
  title: "大气物理学精讲讲义",
  description: "基于银燕教材的大气物理学全公式族谱推导与期末习题精讲",
  lang: "zh-CN",
  base: process.env.GITHUB_REPOSITORY ? `/${process.env.GITHUB_REPOSITORY.split('/')[1]}/` : '/',
  head: [
    ['link', { rel: 'icon', href: 'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌪️</text></svg>' }]
  ],
  markdown: {
    config: (md) => {
      md.use(mathjax3)
    }
  },
  themeConfig: {
    logo: { text: '☁️ 气象物理学' },
    nav: [
      { text: '首页', link: '/' },
      { text: '课程讲义', link: '/chapter_01/Ch01_Sec02_大气的基础知识' },
      { text: '学习进度', link: '/progress' }
    ],
    sidebar: {
      '/': getDynamicSidebar()
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/tg56y2p4/atmospheric-study' }
    ],
    search: {
      provider: 'local'
    },
    outline: {
      level: [2, 3],
      label: '本小节目录'
    },
    footer: {
      message: '云端学术大脑 (Gemini Spark) + 本地执行引擎 (Antigravity) 协同驱动',
      copyright: '南京信息工程大学《大气物理学》（银燕）全公式推导精讲'
    }
  }
})
