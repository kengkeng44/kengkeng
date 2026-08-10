---
name: kengkeng repo (Notion portfolio source-of-truth)
description: kengkeng 桌面 repo 是 Notion portfolio 頁面的 source-of-truth；改內容流程跟 sync 指令位置
type: project
originSessionId: 48c6a45d-8dcc-4d52-a38a-2cf630eb691e
---
`C:\Users\acer\Desktop\kengkeng` 是用戶 Notion 個人 portfolio 頁面的 source-of-truth。

**Notion target page**: `fbb7854a-2f6c-8257-8b1c-012f3b2116ae` (https://www.notion.so/Jen-Ho-Cheng-fbb7854a2f6c82578b1c012f3b2116ae)

**結構**:
- `notion/00-intro.md` 到 `notion/05-contact.md` — 6 個分區檔，依檔名排序串接
- `.claude/commands/sync-kengkeng-to-notion.md` — slash command，跑 `replace_content` 整頁覆蓋

**工作流**: 改 md → 開 `edit/<name>` 分支 → push → merge main → 在 Claude Code 跑 `/sync-kengkeng-to-notion`

**Why**: 用戶在外面沒電腦想更新時，能用 Claude Code 改內容、push GitHub 後再 sync 到 Notion；branch workflow 給自己 review 緩衝。

**How to apply**:
- 用戶要改 Notion portfolio 內容時，引導去改這個 repo 的 md 而不是直接動 Notion
- About 區塊裡的 `<page url="...e557854a...">鄭仁和的使用說明書</page>` 子頁面 tag **絕對不能刪**，否則 `replace_content` 會被 API 擋下（誤刪子頁面保護）
- Notion 用的是 enhanced markdown，toggle 用 `{toggle="true"}`、巢狀用 tab 縮排，不要當一般 GitHub markdown 處理
