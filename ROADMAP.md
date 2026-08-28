# Roadmap — 跨專案總覽

> 這份是**帳號層級的跨專案駕駛艙**:一眼看完 kengkeng44 底下所有專案在哪個階段。
> 細節規劃留各專案 repo(`docs/plans` + `docs/specs`);這裡只放「一句話狀態 + 下一步」。

最後更新:2026-08-28

## 進行中 / 主力

| 專案 | 是什麼 | 狀態 | 下一步 |
|---|---|---|---|
| **Pickup(奶奶的睡前英文童話)** | 兒童 + 親子的家庭 ELT 遊戲。React + Vite + TypeScript,聽讀理解題為核心、童話章節 + 奶奶 voice、慢速 TTS。內容由 cron 持續產出,已到 ch34 | 🟢 已上線,持續迭代 | ① 桌面版手機比例置中(4 檔 6+ fixed 元素)② 題目品質:65 個 mirror-lint warn + 16 個提前揭答 ③ Phaser 層約 7,000 行死碼退休 |
| **Gulu(咕嚕)** | 單機 PWA 英文題庫遊戲,靜態四庫產線 + 冒險明信片 + 圖鑑。題量 959+,建置期守門檢查全開 | 🟢 已上線 | app icon 換新 —— 生成工具與配色(蜂蜜金 on 暮光藍)已就緒,等母圖切尺寸後發布 |
| **kengkeng**(本 repo) | 個人 portfolio 的 source of truth:Notion 頁面 + GitHub profile + Operator's Card 儀表板 | 🟢 維護中 | 儀表板 P2–P4(每專案設定頁 / 現況頁 / 考核頁) |

## 已上線 / 作品集

| 專案 | 是什麼 | Live |
|---|---|---|
| **Olist Brazil E-commerce Analytics** | 從 99,441 筆訂單找出 R$469K 召回機會(ROI 9.4×),RFM 分群 + Cohort 熱力圖 + 分期付款隱形 CRM | [repo](https://github.com/kengkeng44/olist-project) · [demo](https://olist-jenho.streamlit.app/) |
| **Cookie Cats A/B Test** | 第一段就抓出 SRM 異常(p=0.0086),Frequentist + Bootstrap + Bayesian 三角驗證 90K 玩家 | [repo](https://github.com/kengkeng44/cookie-cats-ab-test) · [demo](https://cookie-cats-jenho.streamlit.app/) |
| **ReportRobot** | 每日 LINE 簡報 bot:投資組合、新聞、天氣、AI 分析。Python + Railway,密鑰走 Infisical | [repo](https://github.com/kengkeng44/ReportRobot) |
| **Telegram Bot Workflow Suite** | 連結／截圖一鍵存進 Notion,以及 AI 協作社群文案自動發到 Threads | [repo](https://github.com/kengkeng44/Telegram-Bot-Workflow-Suite-Publishing-Bookmarking) |
| **tw-job-scraper** | 104 人力銀行爬蟲:search API 包裝 + 可組合的 filter pipeline | [repo](https://github.com/kengkeng44/tw-job-scraper) |
| **kengkeng44**(profile README) | GitHub 個人頁,由本 repo 跑 `/sync-kengkeng-to-profile` 推送 | [profile](https://github.com/kengkeng44) |

## 暫停 / 想法池

| 專案 | 是什麼 | 為什麼停 |
|---|---|---|
| **pickup-rn** | Pickup 的 React Native port PoC | 停在 2026-06-09。web 版仍是主力,RN 要等 dev-client build 跑通才續。四個 RN 相關的自動化 cron 也一併暫停中 |

## 圖例

🟢 穩定 / 維護中 · 🟡 進行中 · 🔴 卡住 / 待決策 · ⚪ 想法池(還沒開始)

## 怎麼維護這份

每次某專案狀態變了,回來改那一列。跨專案盤點(掃 repo + 本機 clone、對分支與 PR 逐個查證)可以整批更新這張表。
