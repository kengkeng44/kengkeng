---
description: 把 kengkeng/profile/README.md 推到 GitHub Profile README repo (kengkeng44/kengkeng44),讓 github.com/kengkeng44 個人頁更新
allowed-tools: Bash, Read
---

把 `profile/README.md` 整檔覆蓋到 `kengkeng44/kengkeng44/README.md`,讓 GitHub 個人頁 (github.com/kengkeng44) 頂部顯示最新版自我介紹。

## 目標 repo

- Repo: `kengkeng44/kengkeng44`
- 檔案: `README.md`(預設分支 `master`)
- 觀眾入口: https://github.com/kengkeng44

## 步驟

1. **檢查 git 狀態** — 跑 `git -C "C:/Users/acer/Desktop/kengkeng" status --porcelain --branch`。如果不在 `main`、或 `profile/README.md` 有未 commit 的變更,先告訴用戶,不要擅自繼續。同步前要求本地內容跟 `main` 一致,避免把實驗中版本推上去。

2. **讀本地 profile/README.md** — `Read C:/Users/acer/Desktop/kengkeng/profile/README.md`,把字串記下來。

3. **抓 GitHub 上現有 README 的 SHA** — `gh api repos/kengkeng44/kengkeng44/contents/README.md -q '.sha'`。GitHub Contents API 要靠這個 SHA 做樂觀鎖,沒它不能更新。

4. **base64 encode + PUT 上傳** — 用 PowerShell 把本地內容 base64 化,再呼叫 `gh api -X PUT repos/kengkeng44/kengkeng44/contents/README.md` 帶 `message`、`content`(base64)、`sha`(step 3 取得)、`branch=master`。

   PowerShell 範本:
   ```powershell
   $content = Get-Content -Raw -Encoding UTF8 -Path "C:\Users\acer\Desktop\kengkeng\profile\README.md"
   $b64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content))
   $sha = gh api repos/kengkeng44/kengkeng44/contents/README.md --jq '.sha'
   $body = @{ message = "sync: profile README from kengkeng repo"; content = $b64; sha = $sha; branch = "master" } | ConvertTo-Json -Compress
   $body | gh api -X PUT repos/kengkeng44/kengkeng44/contents/README.md --input -
   ```

5. **報告結果** — 一句話告訴用戶推送成功 + 給他 https://github.com/kengkeng44 連結點開檢查(可能要等 30 秒~1 分鐘 GitHub cache 才會刷新)。失敗就貼 API error 原文,不要自己推測原因。

## 注意

- 目標分支是 `master` 不是 `main`(kengkeng44/kengkeng44 是 GitHub 早期建立的 repo,預設分支仍為 master)。
- 整檔覆蓋。GitHub 上手改 `kengkeng44/kengkeng44/README.md` 的東西會被蓋掉,所有編輯都回到 `kengkeng/profile/README.md`。
- `profile/README.md` 用 GitHub-flavored Markdown(emoji shortcode、`> [!NOTE]` alert、code fence 都認),不要混 Notion 語法(`{toggle="true"}`、`<page url="…">` 之類)— 那些在 GitHub 上會被當成原始文字顯示。
- 跟 `/sync-kengkeng-to-notion` 角色不一樣:
  - `/sync-kengkeng-to-notion` → 把 `notion/00-05*.md` 串起來推到 Notion 頁面
  - `/sync-kengkeng-to-profile` → 把 `profile/README.md` 推到 GitHub 個人頁
  兩個各自獨立,可單獨跑也可前後跑。
