# Roadmap — 跨專案總覽

> 這份是**帳號層級的跨專案駕駛艙**:一眼看完 kengkeng44 底下所有專案在哪個階段。
> 細節規劃留各專案 repo(`docs/plans` + `docs/specs`);這裡只放「一句話狀態 + 下一步」。
> GitHub Projects 看板(帳號層級)是互動版,這份是它的文字底稿與離線備份。

最後更新:2026-07-12

## 進行中 / 主力

| 專案 | 是什麼 | 狀態 | 下一步 |
|---|---|---|---|
| **拾光 / PickRay** | 8–12 兒童 + 親子的家庭 ELT 遊戲(Phaser + React + Vite + Capacitor + TS)。cloze 填空為核心、7 童話 + 奶奶 voice、慢速 TTS、SRS lite。2026-06-05 從「下班族」pivot | 🟡 brainstorming 收尾 | ① CLAUDE.md 收成單一正本(代碼地圖 + 產品設計兩段)② 清掉頂層壞檔名殘骸 ③ 上 private GitHub repo。見 `docs/pickray-setup.md` |
| **kengkeng**(本 repo) | 個人 portfolio 的 source of truth:Notion 頁面 + GitHub profile + Operator's Card 儀表板 | 🟢 維護中 | 把 PM 流程收進 `docs/`(進行中) |

## 已上線 / 作品集

| 專案 | 是什麼 | 狀態 | Live |
|---|---|---|---|
| **Olist Brazil E-commerce Analytics** | 從 99,441 筆訂單找出 R$469K 召回機會(ROID 9.4×),Cohort 熱力圖 + 分期付款隱形 CRM | 🟢 已發布 | [repo](https://github.com/kengkeng44/olist-project) · [demo](https://olist-jenho.streamlit.app/) |
| **Cookie Cats A/B Test** | 第一段抓出 SRM 異常(p=0.0086),Frequentist + Bootstrap + Bayesian 三角驗證 90K 玩家 | 🟢 已發布 | [repo](https://github.com/kengkeng44/cookie-cats-ab-test) · [demo](https://cookie-cats-jenho.streamlit.app/) |
| **kengkeng44**(profile README) | GitHub 個人頁,由 kengkeng repo `/sync-kengkeng-to-profile` 推送 | 🟢 維護中 | — |

## 圖例

- 🟢 穩定 / 維護中 · 🟡 進行中 · 🔴 卡住 / 待決策 · ⚪ 想法池(還沒開始)

## 怎麼維護這份

- 每次某專案狀態變了,回來改這張表的一列(或跑之後可能加的 refresh script)。
- 真正的細節、待辦、bug 用**各 repo 的 GitHub Issues**;跨專案的優先序用**帳號層級 Projects 看板**。
- 這份 `ROADMAP.md` 是給人快速掃的高層地圖,不是待辦清單 —— 別把細碎 todo 塞進來。
- PM 工作流細節見 [`docs/project-management.md`](docs/project-management.md)。
