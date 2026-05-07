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

平常編輯：

```sh
git switch -c edit/<change-name>
# 改 notion/*.md
git commit -am "edit: <what changed>"
git push -u origin edit/<change-name>
# 開 PR、自己 review、merge 進 main
git switch main && git pull
```

合進 main 後在 Claude Code 跑：

```
/sync-kengkeng-to-notion
```

就會把整頁覆蓋成 repo 目前 main 的內容。

## 注意事項

- About 區塊裡的子頁面 `<page url="...e557854a..."> 鄭仁和的使用說明書 </page>` **絕對不能刪**，否則 sync 會被 Notion API 擋下（會誤刪子頁面）。要改文案改外面的文字，內嵌的 page tag 留著。
- `replace_content` 是整頁覆蓋。直接在 Notion 上改的東西會被蓋掉，所有編輯回到 repo 做。
