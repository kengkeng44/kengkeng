"""二層分類:Permissions Allow 依工具家族、Memory 依主題。"""
import re
from collections import defaultdict

FAM_ORDER = [
    "Git", "GitHub CLI (gh)", "Node · npm · wrangler", "Python · pip",
    "PowerShell 系統工具", "檔案 · 搜尋", "Notion MCP", "套件 · 資料工具",
    "網路", "其他",
]


def _fam(p):
    low = p.lower()
    if p.startswith("mcp__"):
        return "Notion MCP"
    if re.match(r"(Bash|PowerShell)\(git ", p):
        return "Git"
    if re.match(r"(Bash|PowerShell)\(gh ", p):
        return "GitHub CLI (gh)"
    if re.search(r"\b(npm|npx|wrangler)\b", low):
        return "Node · npm · wrangler"
    if re.search(r"python|\bpy \b|\bpip |anaconda|pythonio", low):
        return "Python · pip"
    if re.match(r"PowerShell\((Get-|Test-Path|Copy-Item|New-Item|Set-|Add-|Import-Csv)", p):
        return "PowerShell 系統工具"
    if re.search(r"winget|kaggle|jupyter|infisical", low):
        return "套件 · 資料工具"
    if re.search(r"curl|websearch|webfetch", low):
        return "網路"
    if re.match(r"(Bash\((ls|dir|grep|find|where)|Read|Write\()", p):
        return "檔案 · 搜尋"
    return "其他"


def perm_families(allow):
    """回傳 [(family, [items])],依 FAM_ORDER 排序,空群略過。"""
    groups = defaultdict(list)
    for a in allow:
        groups[_fam(a["pattern"])].append(a)
    return [(k, groups[k]) for k in FAM_ORDER if groups.get(k)]


def _topic(m):
    s = (m["name"] + " " + m["description"]).lower()
    if re.search(r"pickup|gulu|fabu|rive|toeic|mochi|咕嚕|拾光|placeholder|listening|emoji|checkmark|bilingual|speech|lesson|narration|audience", s):
        return "Pickup · Gulu 產品規則"
    if re.search(r"hex|圖片|生圖|negative|prompt block|金融|finance", s):
        return "Prompt · 生圖"
    if re.search(r"chinese|telegram|文體|jargon|小白|no-computer|手機|ordering|排第一|proofread|url|explain|溝通", s):
        return "輸出 · 溝通風格"
    if re.search(r"autonomous|quota|notify|push|segment|block|通知|段落|align", s):
        return "Autonomous · 通知 · 節奏"
    if re.search(r"git|github|push|repo|commit|secret|fabricat|dedup|permission|settings|refresh-dashboard|automode|delete|安全", s):
        return "Git · 安全 · 權限"
    if re.search(r"powershell|utf|cp950|bom|anaconda|hermes|subprocess|encoding|conda", s):
        return "環境 · 工具 (Windows)"
    if re.search(r"notion|學習地圖|portfolio source|知識", s):
        return "Notion · 知識 · 學習"
    if re.search(r"olist|reportrobot|threads|kengkeng repo|cleanup|磁碟|disk", s):
        return "專案 · 資料"
    if re.search(r"subscription|profile|career|就業|excel|簡報|slide|使用者", s):
        return "使用者資訊"
    return "其他"


def memory_topics(mem):
    """回傳 [(topic, [items])];少於 3 條的群併入「其他」,最大群在前,其他在最後。"""
    groups = defaultdict(list)
    for m in mem:
        groups[_topic(m)].append(m)
    for k in [k for k in list(groups) if k != "其他" and len(groups[k]) < 3]:
        groups["其他"].extend(groups.pop(k))
    order = sorted(groups, key=lambda k: (k == "其他", -len(groups[k])))
    return [(k, groups[k]) for k in order]
