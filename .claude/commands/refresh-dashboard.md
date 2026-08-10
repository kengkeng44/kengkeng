---
description: 重生 Operator's Card 儀表板(確定性 Python 生成腳本)
allowed-tools: Bash, PowerShell
---

重生本機儀表板並更新桌面捷徑。生成邏輯已改為**確定性腳本**(非 LLM),來源為 `~/.claude` 的 memory + settings.json + `dashboard/data/*.yaml` + 各專案 `.claude`/git 狀態。

跑:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:/Users/acer/Desktop/kengkeng/dashboard/regen.ps1"
```

腳本進入點:`dashboard/generate_dashboard.py`;核心在 `dashboard/generator/`(memory / permissions / skills / projects / render / build)。

## 同步到 GitHub

regen 只寫本機檔案。線上的 Operator's Card(GitHub Pages,`main` 分支 `/` 根目錄)要靠 commit + push 才會更新。跑完上面的腳本後接著:

```powershell
git -C "C:/Users/acer/Desktop/kengkeng" status --short dashboard/index.html
```

**有變更才繼續**(沒輸出就代表冪等跳過,直接結束,不要硬 commit)。有變更時:

```powershell
git -C "C:/Users/acer/Desktop/kengkeng" add dashboard/index.html
```

然後 commit(訊息沿用既有慣例 `dashboard: refresh Operator's Card (變動摘要)`,摘要寫這次實際變的東西,例如 `Ask 15→10`、`memory 47→48`),再 `git -C "C:/Users/acer/Desktop/kengkeng" push origin main`。

紅線:
- **只 `git add dashboard/index.html`**,絕不 `git add .` — 這個 repo 常有其他未追蹤/未 commit 的變更(可能來自另一個並行的 session),那些要由用戶自己決定。
- 直接 commit 到 `main`(此 repo 既有慣例,dashboard 例行同步不開分支)。
- push 完把可點的 URL 單獨一行給用戶:`https://kengkeng44.github.io/kengkeng/dashboard/`

## 自我指涉現象:用「落後幾個 commit」判斷,不要看差異內容

dashboard 會把各專案(含 kengkeng 自己)的最新 commit hash 畫進 `index.html`,所以每次 commit 完 index.html 立刻又過期一次。線上永遠落後 HEAD 一個 commit,這是設計下限不是 bug。

判準**不是**「差異是不是只有 hash」(那條會誤判:別的 session push 過之後,差異同樣只有 hash,但線上是真的落後)。正確判準是**已 commit 的 dashboard 裡記錄的 hash 距離現在的 HEAD 差幾個 commit**:

```powershell
$repo = "C:/Users/acer/Desktop/kengkeng"
$html = git -C $repo show HEAD:dashboard/index.html
$old = [regex]::Match($html, 'kengkeng.{0,600}?proj-meta">([0-9a-f]{7})').Groups[1].Value
git -C $repo rev-list --count "$old..HEAD"
```

- 輸出 **0 或 1** → 自我指涉的正常下限。`git checkout -- dashboard/index.html` 丟掉,不要 commit,否則會無限追。
- 輸出 **2 以上** → 線上真的落後(中間有別的 commit 進來,可能來自並行的 session),照上面的同步流程 commit + push。

若差異不只 kengkeng 自己的 hash(例如 generator 被改出新區塊或新欄位),代表有別的變更正在跑,先查清楚來源再動。

備註:
- 收工時 Stop hook 已會自動跑同一支腳本,通常不需手動。
- 冪等:內容沒變不重寫 `index.html`。
- P4 上線後此腳本會一併 push 到 Cloudflare Pages。
- 舊 LLM 版指令規格已由確定性生成器取代;舊視覺版卡保留為 `dashboard/index.legacy.html`(git 歷史 `b932eee`)。
- 本檔有一份帳號級副本在 `~/.claude/commands/refresh-dashboard.md`。用戶慣例是從家目錄啟動 Claude Code,專案級 `.claude/` 不會載入,實際生效的是帳號級那份;兩份內容需手動保持一致。
