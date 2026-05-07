## 🗂️ Projects 個人專案 {toggle="true"}
	### [🛒 蝦皮台灣 · 賣家費率透明化工具 BRD](/33da06b8c005805cbe09dd2351dfb151?pvs=25)
	> 定位為促銷 GMV 的防禦性投資，而非賣家福利。
	<table fit-page-width="true" header-row="true">
<tr>
<td>項目</td>
<td>內容</td>
</tr>
<tr>
<td>角色</td>
<td>獨立撰寫</td>
</tr>
<tr>
<td>調研來源</td>
<td>ECDB、EasyStore、PTT 賣家社群</td>
</tr>
<tr>
<td>競品對比</td>
<td>Shopee PH/SG、momo、Amazon</td>
</tr>
<tr>
<td>產出</td>
<td>10 章節 BRD（中英雙版），5 項阻斷問題與對應負責方</td>
</tr>
<tr>
<td>規劃</td>
<td>Phase 1 費率試算頁 → Phase 2 SKU 毛利追蹤</td>
</tr>
	</table>
	### [📦 Olist 巴西電商分析 · RFM 找出 R$469K 召回機會 (ROI 9.4×)](https://github.com/kengkeng44/olist-project)
	> 🚀 Live demo: https://olist-jenho.streamlit.app/ · SQL Window Function · 99,441 筆訂單 / 9 張表
	<table fit-page-width="true" header-row="true">
<tr>
<td>項目</td>
<td>內容</td>
</tr>
<tr>
<td>角色</td>
<td>獨立分析</td>
</tr>
<tr>
<td>核心發現</td>
<td>RFM 分群找出 R$469K 召回商機，預估 ROI 9.4×</td>
</tr>
<tr>
<td>方法</td>
<td>SQL NTILE Window Function 分群、Cohort 留存熱力圖、巴西分期付款（Boleto）洞察</td>
</tr>
<tr>
<td>產出</td>
<td>Streamlit 互動 Demo · HTML Dashboard · Tableau · 面試簡報 PDF</td>
</tr>
<tr>
<td>差異化</td>
<td>避開 Online Retail 教學資料撞題，挑巴西市場（Boleto 文化、信用卡分期）得出與歐美不同結論</td>
</tr>
	</table>
	### [🎮 Cookie Cats A/B 測試評估 · 第一段抓出 SRM 異常](https://github.com/kengkeng44/cookie-cats-ab-test)
	> 🚀 Live demo: https://cookie-cats-jenho.streamlit.app/ · Frequentist + Bootstrap + Bayesian · 90,189 玩家
	<table fit-page-width="true" header-row="true">
<tr>
<td>項目</td>
<td>內容</td>
</tr>
<tr>
<td>角色</td>
<td>獨立分析</td>
</tr>
<tr>
<td>核心發現</td>
<td>實驗有 SRM 異常 (χ²=6.90, p=0.0086)，第一段就攔下 — 嚴格不該採信</td>
</tr>
<tr>
<td>方法</td>
<td>Frequentist (chi-square)、Bootstrap、Bayesian 三角驗證</td>
</tr>
<tr>
<td>建議</td>
<td>若硬解讀：gate_40 留存顯著更差 (-0.82pp, P(better)=0.001) → 不要 ship</td>
</tr>
<tr>
<td>展現能力</td>
<td>看 A/B 結果先檢查實驗有效性、知道 p&lt;0.05 不等於 ship、用三方法交叉驗證</td>
</tr>
	</table>
	### [🤖 Telegram Bot 工作流套件 · 發文 + 收藏](https://github.com/kengkeng44/Telegram-Bot-Workflow-Suite-Publishing-Bookmarking)
	> Telegram Bot API · Claude API · Meta Graph · Notion API · 共 5 個 API
	<table fit-page-width="true" header-row="true">
<tr>
<td>項目</td>
<td>內容</td>
</tr>
<tr>
<td>角色</td>
<td>獨立開發</td>
</tr>
<tr>
<td>Publisher 端</td>
<td>Claude 差異化改寫，同步 Threads / FB / IG</td>
</tr>
<tr>
<td>Capture 端</td>
<td>傳連結自動寫入 Notion，收藏縮至兩步</td>
</tr>
<tr>
<td>核心設計</td>
<td>Telegram 為單一入口，整合兩個工作流斷點</td>
</tr>
	</table>
	### [📡 ReportRobot · LINE 每日情報機器人](https://github.com/kengkeng44/ReportRobot)
	> Python · Railway Cron · LINE Messaging API · Claude API · 每天 6:00 自動推播
	<table fit-page-width="true" header-row="true">
<tr>
<td>項目</td>
<td>內容</td>
</tr>
<tr>
<td>角色</td>
<td>獨立開發 + 維運</td>
</tr>
<tr>
<td>每日推播</td>
<td>淡水天氣、國際盤前（Nasdaq / 費半 / TSMC ADR / 黃金）、三大法人買賣超、AI 盤前重點 6-8 條</td>
</tr>
<tr>
<td>互動指令</td>
<td>個股 / ETF / 美股查詢、持倉損益、待辦提醒、AI 自由問答（精簡 + IC Memo 兩檔）</td>
</tr>
<tr>
<td>生產等級補強</td>
<td>HMAC webhook 驗章、log 脫敏、API exponential backoff retry、graceful degradation、排程冪等性</td>
</tr>
	</table>
