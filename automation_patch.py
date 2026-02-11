import os, requests, subprocess
from dotenv import load_dotenv

load_dotenv('/root/agent_system/.env')

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN') # Βεβαιώσου ότι το έχεις στο .env
REPO_OWNER = "Xanoutas" # Το δικό σου GitHub username
REPO_NAME = "AI-Bounty-Solutions"

def reply_to_farcaster(parent_hash, text):
    url = "https://api.neynar.com/v2/farcaster/cast"
    headers = {
        "api_key": os.getenv('NEYNAR_API_KEY'),
        "Content-Type": "application/json"
    }
    payload = {
        "signer_uuid": os.getenv('SIGNER_UUID'),
        "text": text,
        "parent": parent_hash
    }
    r = requests.post(url, json=payload, headers=headers)
    return r.status_code

def check_github_comments():
    print("🔍 Έλεγχος για νέα σχόλια στο GitHub...")
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/comments"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        comments = response.json()
        for comment in comments:
            # Αν το σχόλιο δεν είναι δικό μας και περιέχει εντολή αλλαγής
            if comment['user']['login'] != REPO_OWNER:
                print(f"⚠️ Νέο σχόλιο από {comment['user']['login']}: {comment['body']}")
                # Εδώ θα καλούσαμε τον Auditor να διορθώσει το αρχείο
                # Για την ώρα το στέλνουμε στο Discord
                send_to_discord(f"📢 Σχόλιο στο GitHub: {comment['body']}")

def send_to_discord(msg):
    webhook = os.getenv('DISCORD_WEBHOOK')
    requests.post(webhook, json={"content": msg})

if __name__ == "__main__":
    check_github_comments()
