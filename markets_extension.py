import requests
import feedparser # Θα χρειαστεί: pip install feedparser
import os
from dotenv import load_dotenv

load_dotenv('/root/agent_system/.env')

def scan_algora():
    print("🔍 Σκανάρισμα Algora Bounties μέσω GitHub...")
    # Η Algora χρησιμοποιεί συγκεκριμένα labels στο GitHub
    url = "https://api.github.com/search/issues?q=label:bounty+is:open+org:algora-io"
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            issues = r.json().get('items', [])
            for issue in issues:
                # Εδώ στέλνουμε το task στον Auditor
                title = issue['title']
                link = issue['html_url']
                print(f"🎯 Algora Found: {title}")
                # process_task("Algora", title, issue['body'], link, "github_native")
        else:
            print(f"⚠️ Algora Scan Error: {r.status_code}")
    except Exception as e:
        print(f"❌ Error in Algora scan: {e}")

def scan_gitcoin():
    print("🔍 Σκανάρισμα Gitcoin Bounties via RSS...")
    # Το Gitcoin συχνά δημοσιεύει μέσω RSS/Atom feeds για νέα tasks
    feed_url = "https://gitcoin.co/feed/bounties" # Παράδειγμα endpoint
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            description = entry.summary
            print(f"🎯 Gitcoin Found: {title}")
            # process_task("Gitcoin", title, description, link, "gitcoin_external")
    except Exception as e:
        print(f"❌ Error in Gitcoin scan: {e}")

if __name__ == "__main__":
    scan_algora()
    scan_gitcoin()
