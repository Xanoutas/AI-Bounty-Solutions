import sqlite3, requests, time
from datetime import datetime

# CONFIG
RE_WEBHOOK = "ΒΑΛΕ_ΕΔΩ_ΤΟ_ΝΕΟ_WEBHOOK_ΣΟΥ"
DB_FILE = "/root/agent_system/ioannina_homes.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS listings (id TEXT PRIMARY KEY, price REAL, link TEXT)')
    conn.commit()
    conn.close()

def check_real_estate():
    # Εδώ θα τρέχει το scraping logic (Spitogatos/XE API simulation)
    # Φίλτρα: Ιωάννινα, <= 40000, Floor >= 0
    print(f"[{datetime.now()}] Scanning for homes in Ioannina...")
    
    # Παράδειγμα αποτελέσματος
    found_items = [
        {"id": "re_101", "title": "Ισόγειο Studio Ιωάννινα", "price": 38000, "url": "https://example.com/p101"}
    ]

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for item in found_items:
        c.execute("SELECT id FROM listings WHERE id=?", (item['id'],))
        if not c.fetchone():
            # Νέο ακίνητο!
            c.execute("INSERT INTO listings VALUES (?, ?, ?)", (item['id'], item['price'], item['url']))
            send_to_discord(item)
    conn.commit()
    conn.close()

def send_to_discord(item):
    payload = {
        "embeds": [{
            "title": "🏠 Νέα Ευκαιρία στα Ιωάννινα!",
            "description": f"**{item['title']}**\n💰 Τιμή: {item['price']}€",
            "url": item['url'],
            "color": 0x2ecc71
        }]
    }
    requests.post(RE_WEBHOOK, json=payload)

if __name__ == "__main__":
    init_db()
    while True:
        check_real_estate()
        time.sleep(3600) # Έλεγχος ανά ώρα
