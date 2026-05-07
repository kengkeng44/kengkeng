# kengkeng

我的 Notion 個人 portfolio 頁面 source code。Repo 是 source of truth，跑 `/sync-kengkeng-to-notion` 把內容推到 Notion。

## 同步目標

- Notion page: https://www.notion.so/Jen-Ho-Cheng-fbb7854a2f6c82578b1c012f3b2116ae
- Page ID: `fbb7854a-2f6c-8257-8b1c-012f3b2116ae`

## 結構

```
notion/
  00-intro.md       頁面開頭：tagline + Currently + 「最近在研究」
  01-about.md       About 自我概述
  02-projects.md    Projects 個人專案
  03-skills.md      Skills 技能
  04-experience.md  學歷 & 經歷
  05-contact.md     Contact 聯絡方式
.claude/commands/
  sync-kengkeng-to-notion.md   slash command
```

每個 `.md` 用的是 Notion-flavored markdown（toggle 用 `{toggle="true"}`、tab 縮排表示巢狀）。檔名前綴決定串接順序。

## 工作流（branch-based）

### 在自己這台機器上改

```powershell
cd C:\Users\acer\Desktop\kengkeng

# 1. 開分支
git switch -c edit/<change-name>

# 2. 改 notion/*.md（用 Claude Code 或編輯器）

# 3. commit
git commit -am "edit: <what changed>"

# 4. 合進 main
git switch main
git merge edit/<change-name>

# 5. 在這個資料夾開 Claude Code，跑：
#    /sync-kengkeng-to-notion
```

### 在外面沒這台電腦時

兩條路：

**A. 用 GitHub 網頁 / 手機 App 直接改**

1. 在 GitHub 上開 branch，網頁編輯 `notion/*.md`
2. 開 PR、自己 merge 進 main
3. 回家後 `git pull` 同步，再跑 `/sync-kengkeng-to-notion`

**B. 用其他電腦 clone**

```powershell
gh repo clone kengkeng44/kengkeng
cd kengkeng
# 同上 branch-based 流程
git push -u origin edit/<change-name>
# 回家後 fetch + merge + sync
```

### 第一次 push 到 GitHub（還沒做）

```powershell
gh repo create kengkeng --private --source=. --push
```

### Sync 機制

- `replace_content` 整頁覆蓋。每跑一次都會把 repo `main` 的 6 個 `notion/*.md` 串起來推上去。
- 串接順序由檔名前綴決定（00 → 05），中間用 `\n---\n` 分區。
- Notion 的版本歷史（右上角 ··· → Updates）可以還原。

## 注意事項

- About 區塊裡的子頁面 `<page url="...e557854a..."> 鄭仁和的使用說明書 </page>` **絕對不能刪**，否則 sync 會被 Notion API 擋下（會誤刪子頁面）。要改文案改外面的文字，內嵌的 page tag 留著。
- `replace_content` 是整頁覆蓋。直接在 Notion 上改的東西會被蓋掉，所有編輯回到 repo 做。
