# 專案管理工作流(跨所有 repo)

> 決定:**不開專門的 PM repo**。用 GitHub 內建三層 + 各 repo 內文件,零額外維護。
> 這份說明整套怎麼運作,以及每個部分放哪。

## 三層結構

GitHub 的專案管理不是「一個地方」,是三層各司其職:

```
帳號層級 Projects 看板   ← 跨所有 repo 的總覽(Backlog / In Progress / Done)
        │  拉進各 repo 的 issue
        ▼
各 repo 的 Issues        ← 待辦 / bug / 想法的最小單位,一張一件事
        │  細節展開成
        ▼
各 repo 的 docs/         ← plans + specs(跟 code 一起版控)
```

外加一份 [`ROADMAP.md`](../ROADMAP.md)(本 repo root)當**跨專案高層地圖的文字底稿 / 離線備份**。

## 各層放什麼

### 1. 帳號層級 Projects 看板(要你手動建一次)

這是「所有專案管理放一個地方」的正解。它掛在你 GitHub 帳號、**能跨多個 repo**。

**建立步驟(網頁點一次即可):**
1. 到 `https://github.com/users/kengkeng44/projects` → **New project**
2. 選 **Board** 版型,命名例如 `All Projects`
3. 欄位建議:`Backlog` / `In Progress` / `Review` / `Done`
4. 右上 `⋯` → **Workflows** → 開啟 *Item closed → Done*(issue 一關就自動進 Done)
5. 之後任何 repo 開 issue,在 issue 右側 **Projects** 欄選這個看板,就會出現在總覽

**手機 / 外出時**:GitHub App 直接拖卡片改狀態,不用電腦。

### 2. 各 repo 的 Issues

- 一張 issue 一件事;大的用 **sub-issues** 拆小(issue 內 `Create sub-issue`)。
- commit 訊息或 PR 寫 `Closes #12` → merge 進預設分支時自動關那張 issue。
- **建議 labels**(每個 repo 開一次,或用 GitHub 預設):
  - `bug` · `enhancement` · `idea`(想法池)· `blocked`(卡住)· `docs`
  - 優先序:`P0` / `P1` / `P2`

### 3. 各 repo 的 `docs/`

你已經在做的 superpowers 流程就是這層,保留:
- `docs/**/specs/` — 設計文件(brainstorm 產出的規格)
- `docs/**/plans/` — 逐步實作計畫(checkbox 追蹤)

一張 issue 若需要完整設計,就在 issue 裡連到對應的 spec/plan 檔。**細節在檔案、追蹤在 issue、總覽在看板。**

## 一個新專案的起手式

1. 建 repo(private 起步)。
2. 在 repo 內開 issue 把要做的事拆成幾張。
3. 把這些 issue 加進帳號層級 `All Projects` 看板。
4. 要完整設計的,寫 `docs/specs/YYYY-MM-DD-xxx.md`,issue 連過去。
5. 回本 repo 的 [`ROADMAP.md`](../ROADMAP.md) 加一列。

## 慣例速查

| 想做的事 | 用哪個 |
|---|---|
| 記一個待辦 / bug | 該 repo 的 Issue |
| 跨專案看誰在哪個階段 | 帳號層級 Projects 看板 + `ROADMAP.md` |
| 寫完整設計 / 規格 | 該 repo `docs/specs/` |
| 逐步實作計畫 | 該 repo `docs/plans/` |
| 關掉待辦 | commit 寫 `Closes #N` |

## 參考

- [GitHub Docs — Best practices for Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects)
- [Bitovi — GitHub Projects for Solo Developers](https://www.bitovi.com/blog/github-projects-for-solo-developers)
