---
description: 把 kengkeng/notion 裡的所有區塊推到 Notion portfolio 頁面（整頁覆蓋）
allowed-tools: Bash, Read, mcp__claude_ai_Notion__notion-update-page, mcp__claude_ai_Notion__notion-fetch
---

把 `notion/` 底下所有 `.md` 檔依檔名排序串起來，用 `replace_content` 整頁覆蓋到 Notion portfolio 頁面。

## 目標頁面

- Page ID: `fbb7854a-2f6c-8257-8b1c-012f3b2116ae`
- URL: https://www.notion.so/Jen-Ho-Cheng-fbb7854a2f6c82578b1c012f3b2116ae

## 步驟

1. **檢查 git 狀態** — 跑 `git -C "C:/Users/acer/Desktop/kengkeng" status --porcelain --branch`。如果不在 `main`、或有未 commit 的變更，先回報給用戶確認是否繼續，不要擅自進行。

2. **讀取所有區塊檔** — 依序讀（檔名前綴決定順序）：
   - `notion/00-intro.md`
   - `notion/01-about.md`
   - `notion/02-projects.md`
   - `notion/03-skills.md`
   - `notion/04-experience.md`
   - `notion/05-contact.md`

3. **組合內容** — 把 6 個檔的內容用 `\n---\n` 串起來（每個檔本身結尾已有 `\n`，串接時插入 `---\n` 即可）。

4. **驗證子頁面 tag 還在** — 在組好的字串裡 grep `<page url="https://www.notion.so/e557854a2f6c82d3aa9e013698beaf13">`。**必須存在**，否則 `replace_content` 會被 Notion API 擋下說會誤刪子頁面。如果 tag 不見了，停住、告訴用戶哪個檔案漏了。

5. **覆蓋頁面** — 呼叫 `mcp__claude_ai_Notion__notion-update-page`：
   ```
   page_id: fbb7854a-2f6c-8257-8b1c-012f3b2116ae
   command: replace_content
   new_str: <步驟 3 組好的完整字串>
   properties: {}
   content_updates: []
   ```

6. **報告結果** — 一句話告訴用戶有沒有成功、頁面 URL 給他點開檢查。失敗的話貼 API error 原文，不要自己推測原因。

## 注意

- 整頁覆蓋。Notion 上手改的東西會被蓋掉，所有編輯回到 repo。
- 不要動 `update_properties` / `apply_template`，這個指令只做 `replace_content`。
