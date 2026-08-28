# 拾光 / PickRay — 整理範本(在本機做)

> ⚠️ **2026-08-28 註**:這份是 2026-07 的一次性整理範本,當時專案還叫「拾光 / PickRay」。
> 該做的都做完了 —— 專案現名 **Pickup**,repo 在 `kengkeng44/pickup`(預設分支 `master`),
> 頂層壞檔名殘骸也已清掉。留著是為了裡面的通則(AGENTS.md 複數命名、CLAUDE.md 單一正本),
> 步驟本身不必再跑。

> 拾光的 code 在你桌面(`C:\Users\acer\Desktop\...`),不在雲端環境裡,所以這步要**在你本機開 Claude Code / 編輯器**做。
> 這份是「怎麼整理」的具體步驟 + 範本。做完再上 GitHub。暫時寄放在 kengkeng repo,之後可搬進拾光 repo。

## 一、先修正檔名觀念

- 業界標準是 **`AGENTS.md`(複數 S)** —— 30+ AI 工具(Cursor / Codex / Gemini CLI / Windsurf…)會自動讀。
- **`AGENT.md`(單數)沒有工具會自動讀**,等於一份普通 markdown。若你之前建的是單數,先改名或刪掉。
- **不要按主題把兩個檔切成「代碼地圖 vs 產品設計」**。兩個檔在生態裡都是「agent 簡報」,切開只會造成:非 Claude 工具看不到產品設計,Claude 看不到代碼地圖。

## 二、單一正本:CLAUDE.md 分兩段 section

你的 CLAUDE.md 已經很完整,以它為**唯一 source of truth**。結構長這樣:

```markdown
# 拾光 / PickRay — CLAUDE.md

## 產品設計
- 定位:8–12 兒童 + 親子的家庭 ELT 遊戲(2026-06-05 從「下班族」pivot)
- 美學:Studio Ghibli 暖色手繪、olive 綠 / terracotta 紅(非 Duolingo bright)
- 機制:cloze 填空為核心、5 種題型、7 童話 + 奶奶 voice、慢速 TTS、SRS lite、難度系統
- 客群語氣、TTS 規格、SRS 邏輯…(長的話拆到 docs/product-design.md,見下)

## 代碼地圖
- 技術:Phaser + React + Vite + Capacitor + TypeScript
- `src/scenes/`  — Phaser 場景
- `src/ui/`      — React UI 元件
- `src/data/`    — 題庫 / 童話 / SRS 資料
- `src/store/`   — 狀態管理
- `src/audio/`   — 奶奶 voice / TTS
- `src/react-app/` — React 進入點
- 慣例 / 指令:npm scripts、build/dev 怎麼跑、命名規則…
```

**產品設計太長時**:拆成 `docs/product-design.md`,CLAUDE.md 用一行 import 引進來,主檔保持清爽:

```markdown
## 產品設計
@docs/product-design.md
```

**之後想給別的 AI 工具用**:一條 symlink 收工,不維護兩份 ——
```powershell
# PowerShell(系統管理員)
New-Item -ItemType SymbolicLink -Path AGENTS.md -Target CLAUDE.md
# 或 git bash: ln -s CLAUDE.md AGENTS.md
```

## 三、清掉頂層壞檔名殘骸

你截圖提到頂層有幾個把路徑當檔名的殘骸(像 `C:UsersacerDesktop...`)。清理步驟:

```powershell
cd C:\Users\acer\Desktop\<拾光資料夾>

# 1. 先列出頂層檔案,肉眼確認哪些是殘骸(別急著刪)
Get-ChildItem -File | Select-Object Name, Length

# 2. 確認某個殘骸沒被 code import 到(搜整個 src)
Select-String -Path .\src\*.* -Pattern "殘骸檔名" -SimpleMatch

# 3. 確認無引用後刪除(範例,換成實際檔名)
Remove-Item ".\C`:UsersacerDesktop檔名殘骸"
```

⚠️ 刪之前務必 `git status` 確認這些殘骸沒被追蹤成重要檔;有疑慮先 `git mv` 到 `_trash/` 資料夾,跑一次 build 沒事再真刪。

## 四、上 GitHub(private repo)

在本機拾光資料夾:

```powershell
# 若還沒 init
git init
git add .
git commit -m "chore: restructure CLAUDE.md, clean stray filenames"

# 建 private repo 並推上去(需本機有 gh CLI 且已登入)
gh repo create pickray --private --source=. --push
```

沒有 gh CLI 就先在 github.com 手動建 `pickray`(private),再:
```powershell
git remote add origin https://github.com/kengkeng44/pickray.git
git push -u origin main
```

## 五、收尾接回 PM

上 GitHub 後:
1. 開幾張 issue 把「brainstorming 收尾後的下一步」拆出來(題型、TTS、SRS…)。
2. 把這些 issue 加進帳號層級 `All Projects` 看板(見 `project-management.md`)。
3. 回 `ROADMAP.md` 把拾光那列狀態從 🟡 更新掉。

## Checklist

- [ ] AGENT.md(單數)已改名 / 刪除
- [ ] CLAUDE.md 收成單一正本,分「產品設計 / 代碼地圖」兩段
- [ ] (選)長的產品設計拆到 `docs/product-design.md` 並 `@import`
- [ ] 頂層壞檔名殘骸已清
- [ ] 拾光 private repo 已建、已 push
- [ ] issue 開好、加進看板
- [ ] `ROADMAP.md` 狀態已更新
