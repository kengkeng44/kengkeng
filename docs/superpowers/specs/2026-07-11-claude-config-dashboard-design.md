# Claude Code 設定儀表板 — 設計文件

- 日期：2026-07-11
- 狀態：設計已對齊(§1-§12 全數確認),待使用者最終過目 → 進實作計畫
- 位置：`Desktop/kengkeng/dashboard/`(擴充現有 Operator's Card,不新建平行專案)

## 1. 目標

把使用者**所有 Claude Code 的設定與規範**整理成一個隨時可看的視覺化儀表板,並下鑽到每個專案。桌面放捷徑一鍵開啟,收工時自動更新,手機也能私密查看。

## 2. 背景與現況

已存在一套 `Desktop/kengkeng/dashboard/index.html`(1677 行,標題「Operator's Card · Jen-Ho's Claude Code Config」),涵蓋**全域**的 Memory / Permissions / Skills 三塊,由 slash command `/refresh-dashboard`(LLM 驅動)重生並 push。

本專案是**擴充它**,補上三個缺口:
1. 桌面捷徑(目前沒有本機入口)
2. 收工自動更新(目前手動跑指令)
3. 各專案子儀表板(目前只有全域,沒有 per-project)

kengkeng repo 已在 GitHub(`kengkeng44/kengkeng`,**private**)。

## 3. 已鎖定的決策

| 決策 | 選擇 |
|------|------|
| 蓋新的 vs 擴充現有 | 擴充現有 Operator's Card |
| 子儀表板內容 | 設定/規範 **與** 專案現況都要,**拆兩個頁面** |
| 更新觸發 | Stop hook,每次收工自動重生 |
| 放哪看 | 本機(桌面捷徑)+ 發佈私有 web(手機) |
| 手機私有方式 | Cloudflare Pages + Cloudflare Access(email 閃登) |
| 專案範圍 | 自動掃所有有 `.claude/` 或 `CLAUDE.md` 的資料夾 |

自動掃到的專案(2026-07-11):`cheng.robot`、`gulu`、`kengkeng`、`pickup-rn`、`wordwar`。

## 4. 架構:三頁靜態網站

單一資料夾、CSS/JS 內嵌、瀏覽器直開、無需 server(業界標準做法,亦即現有 card 的做法)。

| 頁面 | 內容 | 資料來源 |
|------|------|---------|
| `index.html`(Hub) | 全域 Operator's Card(Memory / Permissions / Skills)+ 專案總覽格 + 導覽列 | `~/.claude/settings.json`、`~/.claude/.../memory/`、`dashboard/data/*.yaml` |
| `config.html`(設定/規範) | 每專案一張卡:專屬 `CLAUDE.md`、`.claude/` 規範摘要、該專案權限 | 各專案 `.claude/`(自動讀) |
| `status.html`(專案現況) | 每專案一張卡:描述、deploy 網址、git 最近 commit/分支/未存改動、待辦、近況 | git(自動)+ `dashboard/data/projects.yaml`(手動欄位) |

導覽:三頁共用頂部導覽列互相跳轉。Hub 的專案格點擊可跳到該專案在 config/status 的錨點。

## 5. 生成管線(核心)

**關鍵轉折**:現有 `/refresh-dashboard` 是 LLM 驅動,無法從 Stop hook 自動跑(hook 只能執行 shell、沒有 LLM)。因此新增一支**確定性生成腳本** `dashboard/generate_dashboard.py`:

輸入:
- 全域:`settings.json`、`memory/*.md` + `MEMORY.md`、`data/priorities.yaml`、`data/perm-descriptions.yaml`、`data/skills.yaml`
- 每專案(自動掃):`.claude/`、`CLAUDE.md`、`git log -1` / `git status` / `git branch`
- 每專案(手動):`data/projects.yaml` — 存無法自動推導的欄位(deploy URL、描述、待辦、近況)

輸出:
- `index.html` / `config.html` / `status.html`(本機)
- 確保桌面捷徑存在
- push 到 Cloudflare Pages

視覺:沿用現有 `index.html` 的設計語言,把它抽成模板 + 資料注入,避免外觀退步。

**資料自動 vs 手動的界線**(對應「自動更新」的真實範圍):
- 設定/規範頁 = 100% 從檔案自動長出,永遠即時
- 專案現況頁 = git 與路徑類自動;deploy URL / 待辦 / 描述類需 `projects.yaml` 維護(由使用者或 Claude 在該專案工作時更新)

## 6. 更新機制

`settings.json` 新增 Stop hook(與現有 `backup-memory.ps1` 並排):

```
Stop → generate_dashboard.py
  ├─ 重生 3 個本機 HTML
  ├─ 確保/更新桌面捷徑
  └─ push Cloudflare Pages
```

保留 `/refresh-dashboard` 作為手動觸發的別名(呼叫同一支腳本)。

## 7. 桌面捷徑

`C:\Users\acer\Desktop` 放一個 `.url`(或 `.lnk`)指向本機 `dashboard/index.html`。生成腳本負責在缺失時重建,不覆蓋使用者可能的自訂。

## 8. 私有發佈(Cloudflare Access)

- Cloudflare Pages 專案託管 `dashboard/`(靜態)
- 套 Cloudflare Access application:policy = 只允許使用者本人 email
- 需**使用者手動**在 Cloudflare 後台一次性設定(建立 Pages 專案 + Access 應用 + 加 email);腳本只負責 push 內容

## 9. 分階段

- **P1**:`generate_dashboard.py` 重建現有全域 Operator's Card(資料驅動)+ Stop hook + 桌面捷徑。里程碑:收工後本機 `index.html` 自動更新、桌面點得開。
- **P2**:`config.html` 每專案設定頁。
- **P3**:`status.html` 每專案現況頁 + `projects.yaml` 資料模型。
- **P4**:Cloudflare Pages + Access 私有發佈。

每階段可獨立驗收。

## 10. 風險與注意

- **隱私**:儀表板含全部 memory/權限/專案內幕,**嚴禁公開發佈**。P4 一律走 Cloudflare Access。本機檔與 GitHub private repo 不受影響。
- **視覺退步**:P1 改成腳本生成時務必比對現有 `index.html` 外觀。
- **hook 效能**:生成 + push 掛在 Stop,需非阻塞(`async`)且加 timeout,避免拖慢收工。
- **push 頻率**:每次收工 push 會產生頻繁 commit;可在腳本內判斷「內容有變才 push」。
- **捷徑安全**:`.url` 指向本機路徑,不含任何密鑰。

## 11. 明確排除(YAGNI)

- 不做即時 live server / websocket
- 不做編輯功能(儀表板唯讀,改設定仍在原始檔)
- 不納入沒有 `.claude/` 或 `CLAUDE.md` 的資料夾

## 12. 考核機制:規範遵循度 Scorecard(待使用者確認)

需求原話:「還要有考核機制,弄得完善一點、規範一點」+「生出來的東西要符合規範」。
→ 把累積的 memory 規範當考核標準,查**實際產出**有無遵循,不合規扣分亮燈。

### 12.1 三種檢查方式(依可驗證性分類)

| 方式 | 適用規範範例 | 誰查 | 頻率 |
|------|-------------|------|------|
| 🤖 自動(腳本判定) | Pickup 題目禁 emoji、git 用 `-C`、.ps1 BOM、正確答案禁 ✓ | `generate_dashboard.py` | 每次收工 |
| 🧑‍⚖️ AI 判定(需語意理解) | 技術說明小白化、無英譯腔、雙語 UI、prompt 品質 | `normal-janitor` 類 audit agent | 按需/定期 |
| ✍️ 自陳(只有使用者知道) | deploy 有無自我驗證等 | 使用者打勾 | 手動 |

原則:主觀規範**不可**硬塞給腳本(會產生假綠燈)。

### 12.2 評分量表

- 每考核項:通過/警告/違規 → 綠/黃/紅(沿用 `priorities.yaml`)
- 每專案:遵循分 = 通過項 ÷ 適用項 → A(≥90%)/B(75-89%)/C(60-74%)/D(<60%)
- 全域:加權總分,Hub 頂部大燈號

### 12.3 呈現

- Hub:全域總分 + 各專案燈號
- 新增第 4 頁 `audit.html`:每條規範一列(對象/檢查方式/結果/扣分原因,可點到違規檔行)
- 專案卡角落顯示 A/B/C/D 徽章

### 12.4 標準來源:`rubric.yaml` 規則目錄(採 linter catalog schema)

新增 `dashboard/data/rubric.yaml`,為考核唯一標準檔,與 memory 一一對齊。每條採業界 linter 規則目錄欄位:

```yaml
- id: pickup-no-emoji-qa
  rule: "題目與選項禁 emoji"
  scope: pickup-rn          # global 或專案名
  severity: error           # error 違規扣滿 / warn 只提醒不扣
  check: auto               # auto腳本 / ai判定 / attest自陳
  detector: "grep emoji in lessons-*.json question|options"
  fix: "移除該欄位 emoji"     # 可修建議
  weight: 3
  waiver: null              # 例外:填 {reason, until} 就不扣分
```

### 12.5 歷史趨勢

每次考核存一筆(日期→分數),`audit.html` 畫趨勢線,追蹤遵循度隨時間變化。

### 12.6 waiver 例外機制(已採用)

規則可對特定專案標記豁免:`waiver: {reason: "wordwar 為實驗場", until: 2026-12-31}`。豁免項在 audit.html 以灰色「已豁免」呈現、不計入扣分,但仍列出以保留可視性。避免刻意的例外被誤判成違規。

### 12.7 規範預算指標(已採用)

Hub 顯示「目前 active 規範數 vs LLM 可靠遵循上限(~150 條指令)」。依研究:前沿 LLM 可靠遵循約 150-200 條、扣系統佔用剩 ~100-150;規範過量反而被忽略。超過門檻亮黃/紅,提醒瘦身或把專案專屬規範下放到 `.claude/rules/`(見 12.9)。

### 12.8 研究依據(2026-07-11 上網學習)

- **Linter 規則目錄**(ESLint / ast-grep):規則 = id + severity(off/warn/error)+ note可修建議 + glob + autofix + waiver;純文字 + metadata 為 source of truth。→ 定義 §12.4 schema。
- **Scorecard 分級**(Port.io):gold/silver/bronze 漸進 > 二元 pass/fail;掉閾值→通知、可申請例外、季度複審門檻。→ A-D 分級 + §12.6 waiver。
- **Compliance Dashboard 版面**(MetricStream / EOXS):三段式 Headline KPI → Trends → Details,每頁 ≤10-15 widget。→ 驗證 Hub→趨勢→audit.html 結構。
- **CLAUDE.md 最佳實踐**:指令預算 ~150 條上限、重要規範置頂、可模組化。→ §12.7 規範預算。

### 12.9 未來可選優化(非本專案範圍)

Claude Code 2.0.64+ 原生支援 `.claude/rules/` 路徑範圍規則。可把專案專屬規範(如 Pickup 系列)從全域 memory 下放到各專案 `.claude/rules/`,只在該專案生效,省全域指令預算。列為 backlog,不在 P1-P4 內。

### 12.10 已確認(取代原待確認)

- 架構:三類檢查 + A/B/C/D + 第 4 頁 `audit.html` + 趨勢線 → 採用
- 第一版:先做「可自動查」的 5-8 條規範,AI 判定 / 自陳類第二批再加 → 採用
- 升級:waiver 例外(§12.6)+ 規範預算指標(§12.7)→ 採用
- 不採用:考核分數掉級 Telegram 通知(使用者婉拒)

## 13. 進度快照(2026-07-11 收尾,重開機前)

**已鎖定**:§3 全部決策 + §12 考核機制(含研究依據、waiver、規範預算,全數確認)。
**待辦**:
1. 使用者最終過目 spec
2. 進 `superpowers:writing-plans` 產實作計畫(P1→P4,見 §9)
3. 依計畫實作,P1 先做:`generate_dashboard.py`(重建現有全域卡)+ Stop hook + 桌面捷徑

**其他 in-flight(與本專案獨立)**:
- pm-skills plugin 已在 `settings.json` 設 `false`(移除 Atlassian 認證黃字),**重開機後生效**;其他 15 plugin 未動。
- Telegram MCP server 顯示 `failed`(另一問題,尚未處理)。
- 本 session 動過 `settings.json`,依規則待跑 `/refresh-dashboard` 同步 Operator's Card。
