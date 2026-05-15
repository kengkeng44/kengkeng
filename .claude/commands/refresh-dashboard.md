---
description: 把 ~/.claude memory + settings.json + dashboard/data/*.yaml 的最新內容重新生成 dashboard/index.html、給用戶看 diff,確認後 commit + push
allowed-tools: Bash, Read, Write, Edit, Glob
---

把 Operator's Card dashboard 重新生成。每次用戶新增 / 修改 memory、調整 settings.json 權限、或更新 skills.yaml 之後跑這個指令把 `dashboard/index.html` 同步到最新。

## 觸發時機

- 用戶新增 / 修改 / 刪除 ~/.claude/.../memory/ 底下任何 .md 後
- 用戶調整 ~/.claude/settings.json 的 permissions 後
- 用戶手動更新 dashboard/data/skills.yaml 後
- 用戶手動打 /refresh-dashboard

## 資料來源

### 1. Memory 條目

- **Index**: `C:\Users\acer\.claude\projects\C--Users-acer\memory\MEMORY.md`(條目清單,順序為呈現順序)
- **個別檔**: 同資料夾下 `*.md`(frontmatter 含 `name`/`description`/`type`,body 是說明文字)

讀取流程:
1. Read MEMORY.md → 解析每行 `- [Title](filename.md) — hook` 取出 filename 與順序
2. 對每個 filename Read 該 .md → 解析 frontmatter + body
3. body 內 `**Why:**` / `**How to apply:**` 段可省略,只取主要 rule 描述
4. 同時準備英文版描述(可以用 frontmatter `description` 翻譯,或從 body 抽)

### 2. Permissions

讀 `C:\Users\acer\.claude\settings.json` 取得 `permissions.allow` 與 `permissions.ask` 兩個陣列。

### 3. Skills

讀 `C:\Users\acer\Desktop\kengkeng\dashboard\data\skills.yaml`,結構:
```yaml
custom:
  - { id, name, en, zh }
  ...
docs: [...]
super: [...]
```

### 4. Priorities

讀 `C:\Users\acer\Desktop\kengkeng\dashboard\data\priorities.yaml`,結構:
```yaml
<filename-no-ext>: red | yellow | green
```

### 5. Permission descriptions + pair merge rules

讀 `C:\Users\acer\Desktop\kengkeng\dashboard\data\perm-descriptions.yaml`,結構:
```yaml
pairs:
  - { primary, alt, en, zh, search }
  ...
descriptions:
  "<pattern>": { en, zh, search }
  ...
```

`pairs` 列的兩個 pattern 在 settings.json 裡同時存在時,合併為一張卡。剩下的 pattern 各自一張卡。

## 生成規則

### Memory cards(panel#memory 的 .cards-grid 內)

每條 memory 一張 `<article class="card t-{TYPE}" data-type="{TYPE}" data-search="{SEARCH_TOKENS} {FILENAME_NO_EXT}">` 卡。
- `TYPE`: feedback / project / user / reference(從 frontmatter `type` 取)
- `SEARCH_TOKENS`: 從 name + description + body 萃取關鍵字(小寫、空白分隔)
- 卡內: type-dot + EN title + ZH title + chev + body(en-desc / zh-desc / filename)

EN title / ZH title:
- ZH title 取 frontmatter `name`(它是中文)
- EN title 翻譯一個簡短的英文版(例: 「Secret 處理規則」→「Secret-Handling Discipline」)

EN desc / ZH desc:
- ZH desc 取 body 主規則段(略過 Why / How to apply)
- EN desc 翻譯一個對應版本

### Permissions cards(panel#perms)

對 Allow 與 Ask 各跑一遍:
1. 從 settings.json 取陣列
2. 對每個 pattern 查 `pairs` 表 — 若該 pattern 在某 pair 的 primary 位置,**合成一張卡**(對應 alt 也吃掉)
3. 剩下的 pattern 查 `descriptions` 表取 en/zh/search
4. 沒在 descriptions 表內的 pattern → fallback: 用 pattern 字串當 search、en 空、zh 「(尚無描述,請至 perm-descriptions.yaml 補)」

合併卡 HTML:
```html
<div class="perm-item card t-allow" data-type="allow" data-search="{search}">
  <div class="perm-head"><span class="type-dot"></span><span><code>{primary}</code><span class="alt-code">+ {alt}</span></span><span class="chev">▸</span></div>
  <div class="perm-body"><div class="perm-body-inner"><span class="en">{en}</span>{zh}</div></div>
</div>
```

單卡 HTML(同上但無 `.alt-code` span)。

### Skills cards(panel#skills 三個 .skill-group)

對 skills.yaml 的 `custom` / `docs` / `super` 各跑一遍。
- custom: id 不帶 namespace 前綴
- docs: id 顯示為 `<span class="ns">document-skills:</span>id`
- super: id 顯示為 `<span class="ns">superpowers:</span>id`
- type class: `t-custom` / `t-docs` / `t-super`

### Stats / tabs / panel-meta 的數字

- Memory count = 上面 memory list 長度
- Allow count = settings.json `permissions.allow` 長度(**不**用合併後的視覺卡數,要原始數)
- Ask count = settings.json `permissions.ask` 長度
- Skills count = 3 群 yaml 加總

更新地方:
- `.stats` strip 四個 `.n` 數字
- 三個 `.tab` 的 `.ct` span 內數字(memory / allow+ask 加總 / skills)
- 三個 `.panel-meta` 的描述

### JS PRIORITY map

在 `<script>` IIFE 內 `const PRIORITY = { ... }` 區塊,根據 priorities.yaml 重建。key 是 data-search 的前綴字串(以 memory 對應卡的 search 為準),value 是 red/yellow/green。

實作: 對每條 memory,取 data-search 的前 2-3 個關鍵字當 key。

## 執行步驟

1. **讀全部資料** — 用 Glob + Read 把上述 5 個資料來源全部讀進來。
2. **生成新內容** — 在記憶中組好 memory cards / allow cards / ask cards / skills cards / stats / tabs / panel-meta / PRIORITY map 的 HTML 字串。
3. **更新 dashboard/index.html** — 用 Edit tool 對 index.html 做 8 次替換:
   - Memory cards 區塊(panel#memory 的 .cards-grid 內 articles)
   - Allow perm-list 內 perm-item 們
   - Ask perm-list 內 perm-item 們
   - Skills custom group 的 .cards-grid 內 articles
   - Skills docs group 的 .cards-grid 內 articles
   - Skills super group 的 .cards-grid 內 articles
   - Stats / tabs / panel-meta 的計數
   - JS PRIORITY map
   
   每次 Edit 用足夠長的 old_string 鎖定區段(可用區段前後的 HTML 結構標記當錨點)。
4. **顯示 diff** — `git -C "C:/Users/acer/Desktop/kengkeng" diff --stat dashboard/index.html` 給用戶看,問是否 commit。
5. **commit + push** — 用戶確認後:
   ```
   git -C "C:/Users/acer/Desktop/kengkeng" add dashboard/index.html
   git -C "C:/Users/acer/Desktop/kengkeng" commit -m "refresh: dashboard regenerated from current memory / settings / skills.yaml"
   git -C "C:/Users/acer/Desktop/kengkeng" push origin main
   ```
6. **報告結果** — 一句話告訴用戶 diff 推送成功 + commit hash。

## 注意事項

- **保留靜態結構**: 只重生「卡片 cards 」+「計數 numbers」+「PRIORITY map」三類動態內容。HTML <head>、<style>、<script> 主體(除 PRIORITY map 外)、hero、footer 全部不要動。
- **不要動 settings.json** — 這個指令只讀,不寫。
- **不要動 memory MD 檔** — 同上。
- **失敗就回報** — 任何 yaml parse 失敗、settings.json 找不到、HTML 結構對不上,**停下來告訴用戶**,不要硬補。
- **diff 大時讓用戶 review** — 如果 diff 超過 200 行,先給用戶看 `--stat` 摘要再決定要不要展開全 diff。
- 如果 dashboard/index.html 沒實質變動(規範化後跟原檔一樣),**不要做空 commit**,直接告訴用戶「已是最新」。
