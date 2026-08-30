---
description: 重生 Operator's Card 儀表板(確定性 Python 生成腳本)
allowed-tools: Bash, PowerShell
---

重生本機儀表板並更新桌面捷徑。生成邏輯為**確定性腳本**(非 LLM),來源為 `~/.claude` 的 memory + settings.json + `dashboard/data/*.yaml` + 各專案 `.claude`/git 狀態。

跑:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:/Users/acer/Desktop/kengkeng/dashboard/regen.ps1"
```

腳本進入點:`dashboard/generate_dashboard.py`;核心在 `dashboard/generator/`(memory / permissions / skills / projects / render / build)。

⚠️ **腳本印的 `[dashboard] wrote ...` 不代表檔案真的被改**。那行 print 是無條件執行的,
真正的寫入判斷在 `generator/build.py:50`(內容相同就不寫)。要確認有沒有更新看 mtime:

```bash
stat -c "%y" "C:/Users/acer/Desktop/kengkeng/dashboard/index.html"
```

## 絕對不要 commit index.html(隱私紅線)

`dashboard/index.html` 含 **memory 全文、完整權限清單、`defaultMode` 狀態、職涯與雇主描述**,
而 `kengkeng44/kengkeng` 是 **PUBLIC repo**。2026-08-28 已 `git rm --cached` 移出版控,
`.gitignore:12` 擋著它,線上 `https://kengkeng44.github.io/kengkeng/dashboard/` 現在回 **404 —— 這是正確狀態,不是壞掉**。

- regen 後**只 commit 生成器程式碼**(`dashboard/generator/`、`generate_dashboard.py`、`data/*.yaml`、`tests/`)
- 絕不 `git add dashboard/index.html`,也絕不 `git add .`
- 不要為了「讓線上有東西看」把它加回去 —— 那等於把整份 memory 公開到網路上

## 要在手機看 → 走 Artifact,不走 GitHub Pages

私密儀表板固定在這條連結(claude.ai 登入才看得到):
`https://claude.ai/code/artifact/26c9e6b1-1414-44a9-9a27-45e79f2ca0f6`

重發流程:
1. 跑上面的 regen 更新本機 `index.html`
2. 從 `index.html` 抽 `<style>` + `<body>` 內容轉成片段(去掉 doctype / html / head / body 標籤),存成 `dashboard-artifact.html`
3. 呼叫 Artifact tool 時**必須帶 `url=` 上面那條連結** —— 沒帶會另開一條新的,舊連結就散了

Stop hook 只更新本機檔,**不會**自動重發 Artifact,要手動跑這步。
mtime 沒動就不用重發,重發也只是刷同樣的東西。

備註:
- 收工時 Stop hook 已會自動跑同一支腳本,通常不需手動。
- 冪等:內容沒變不重寫 `index.html`。改 memory **內文**不會讓儀表板變 —— 它只渲染名稱 / 描述 / 數量 / 分類,改 body 不影響產出。
- 原本的「自我指涉現象」章節(commit 完 index.html 立刻又過期、要算落後幾個 commit)已隨「不進版控」自然消失,不再需要那套判斷。
- 舊視覺版卡保留為 `dashboard/index.legacy.html`(git 歷史 `b932eee`),同樣不進版控。
- 本檔有一份帳號級副本在 `~/.claude/commands/refresh-dashboard.md`。用戶慣例是從家目錄啟動 Claude Code,專案級 `.claude/` 不會載入,實際生效的是帳號級那份;兩份內容需手動保持一致。
