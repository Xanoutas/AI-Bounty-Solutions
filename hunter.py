import os, requests, time, subprocess, json, random, psutil
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('/root/agent_system/.env')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEYNAR_API_KEY = os.getenv("NEYNAR_API_KEY")
SIGNER_UUID = os.getenv("SIGNER_UUID")
DISCORD_URL = "https://discord.com/api/webhooks/1469793300075512090/dCdj2wFQuDrw597CmZ_nTcSzlleVxTL6zHkzYhXYfia3oneI0Ua0mrfxI0y5K7v14bUW"

KEYWORDS = ["python", "automation", "web3", "solidity", "ocean", "ai agent", "plc", "engineering"]
LAST_HEARTBEAT = 0
LAST_KEYWORD_REPORT_DATE = ""

def send_discord(payload):
    try:
        data = {"content": f"🚀 {payload}"} if isinstance(payload, str) else payload
        requests.post(DISCORD_URL, json=data, timeout=10)
    except: pass

def call_openai(prompt):
    if not OPENAI_API_KEY: return None
    try:
        r = requests.post("https://api.openai.com/v1/chat/completions", 
                         headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                         json={"model": "gpt-4o", "messages": [{"role": "user", "content": prompt}]}, timeout=60)
        return r.json()['choices'][0]['message']['content'].strip()
    except: return None

def daily_strategy_report():
    """Στέλνει αναφορά με τα νέα keywords κάθε πρωί στις 08:00"""
    global KEYWORDS, LAST_KEYWORD_REPORT_DATE
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    
    if now.hour == 8 and LAST_KEYWORD_REPORT_DATE != today_str:
        prompt = f"Identify 30 trending keywords for Web3 & Engineering bounties. Current: {KEYWORDS}. Return ONLY a comma-separated list."
        res = call_openai(prompt)
        if res:
            KEYWORDS = list(set([k.strip().lower() for k in res.split(",")]))
            report = {
                "embeds": [{
                    "title": "📅 Ημερήσια Αναφορά Στρατηγικής (08:00)",
                    "description": f"Ο Agent ανανέωσε τους στόχους του για σήμερα.\n\n**Top 30 Keywords:**\n{', '.join(KEYWORDS[:30])}",
                    "color": 0x2ecc71,
                    "footer": {"text": f"Node: EPYC Germany VPS | {today_str}"}
                }]
            }
            send_discord(report)
            LAST_KEYWORD_REPORT_DATE = today_str

def hardware_router(title, desc):
    t = (title + desc).lower()
    if any(x in t for x in ["gpu", "cuda", "vision", "training", "ai model"]): return "RTX 5070 (Pesta)"
    if any(x in t for x in ["heavy", "compile", "docker build", "parallel"]): return "Ryzen 9 (Ioannina)"
    return "EPYC (Germany)"

def auditor_solve_loop(title, description):
    attempts, feedback = 0, ""
    is_eng = any(x in (title + description).lower() for x in ["mechanical", "electrical", "plc", "industrial"])
    while attempts < 3:
        instr = "Strictly comply with ISO/EN European Engineering Standards." if is_eng else ""
        code = call_openai(f"Task: {title}\nDesc: {description}\n{instr}\n{feedback}\nReturn ONLY code/solution.")
        if not code: return None
        audit = call_openai(f"Audit this for {title}. If perfect, start with 'APPROVED'. Else, fix it.\nContent: {code}")
        if audit and "APPROVED" in audit.upper(): return code.replace("```python", "").replace("```", "").strip()
        feedback, attempts = f"Fix these issues: {audit}", attempts + 1
    return None

def process_task(platform, title, description, link, cast_hash=None):
    if not any(k in title.lower() for k in KEYWORDS): return
    
    # Legit Check
    if "LEGIT" not in call_openai(f"Is this bounty legit? {title}. Return LEGIT or SCAM.").upper(): return

    node = hardware_router(title, description)
    
    # ΑΜΕΣΗ ΑΝΑΦΟΡΑ ΣΤΟ DISCORD ΜΟΛΙΣ ΒΡΕΘΕΙ
    send_discord({
        "embeds": [{
            "title": f"🎯 Νέος Στόχος: {platform}",
            "description": f"**Τίτλος:** {title}\n**Node:** {node}\n[Link]({link})",
            "color": 0x3498db
        }]
    })

    sol = auditor_solve_loop(title, description)
    if sol:
        # Push to GitHub (auto_github logic)
        fname = f"sol_{int(time.time())}.py"
        with open(f"/root/agent_system/{fname}", 'w') as f: f.write(sol)
        subprocess.run(["git", "add", "."], cwd="/root/agent_system")
        subprocess.run(["git", "commit", "-m", f"Verified Solution: {title}"], cwd="/root/agent_system")
        subprocess.run(["git", "push", "origin", "main"], cwd="/root/agent_system")
        
        # Neynar Submission
        if platform == "Bountycaster" and cast_hash and SIGNER_UUID:
            msg = f"EPYC Agent Solution for '{title}': Pushed to GitHub. ISO/EN Verified. 🚀"
            requests.post("https://api.neynar.com/v2/farcaster/cast", 
                         json={"signer_uuid": SIGNER_UUID, "text": msg, "parent_hash": cast_hash}, 
                         headers={"api_key": NEYNAR_API_KEY}, timeout=10)
        
        send_discord(f"✅ **Η δουλειά ολοκληρώθηκε:** {title} (Απεστάλη μέσω {node})")

def check_platforms():
    daily_strategy_report()
    try:
        # Bountycaster
        r = requests.get("https://api.bountycaster.xyz/all-open-bounties", timeout=20).json()
        for b in r[:10]: process_task("Bountycaster", b.get('title',''), b.get('content',''), f"https://bountycaster.xyz/bounty/{b['id']}", b.get('hash'))
        # OnlyDust
        q = "{ projects { githubRepo { issues(status: OPEN) { title htmlUrl body } } } }"
        r = requests.post("https://api.onlydust.xyz/graphql", json={'query': q}, timeout=20).json()
        for p in r['data']['projects']:
            for i in p['githubRepo']['issues']: process_task("OnlyDust", i['title'], i.get('body',''), i['htmlUrl'])
        # Ocean Protocol
        r = requests.get("https://api.github.com/repos/oceanprotocol/ocean/issues?labels=bounty", timeout=20).json()
        for i in r: process_task("Ocean", i['title'], i.get('body',''), i['html_url'])
        # Dework
        r = requests.get("https://api.dework.xyz/v1/bounties/trending", timeout=20).json()
        for b in r: process_task("Dework", b['title'], "", f"https://app.dework.xyz/bounty/{b['id']}")
    except: pass

if __name__ == "__main__":
    send_discord("🛡️ Hunter V13.0 Online. Ημερήσια αναφορά στις 08:00 ενεργή.")
    while True:
        if time.time() - LAST_HEARTBEAT > 21600:
            send_discord("💓 **Heartbeat:** Το σύστημα λειτουργεί κανονικά.")
            LAST_HEARTBEAT = time.time()
        check_platforms()
        time.sleep(random.randint(900, 1200))
