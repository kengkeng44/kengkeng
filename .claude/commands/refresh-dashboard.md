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

備註:
- 收工時 Stop hook 已會自動跑同一支腳本,通常不需手動。
- 冪等:內容沒變不重寫 `index.html`。
- P4 上線後此腳本會一併 push 到 Cloudflare Pages。
- 舊 LLM 版指令規格已由確定性生成器取代;舊視覺版卡保留為 `dashboard/index.legacy.html`(git 歷史 `b932eee`)。
