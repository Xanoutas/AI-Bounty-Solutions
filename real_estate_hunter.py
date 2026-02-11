import requests
from bs4 import BeautifulSoup
import sqlite3
import json
import os

# Webhooks που μου έδωσες
WEBHOOK_IOANNINA = "https://discord.com/api/webhooks/1470842715125186766/xT6wq23qM6lEbHGBs5mJ0IYe2jv7qmbBQlR8cB3zII5_V-Jf8YHbO0_mnzCQ1Lrva1FM"

def notify_discord_re(webhook_url, content):
    requests.post(webhook_url, json={"content": content})

def save_to_db(data):
    conn = sqlite3.connect('/root/agent_system/real_estate.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO listings (title, price, sq_meters, price_per_sqm, floor, year_built, location, property_type, url, platform)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['title'], data['price'], data['sq_meters'], data['price_per_sqm'], data['floor'], data['year_built'], data['location'], data['type'], data['url'], 'Spitogatos'))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False # Ήδη υπάρχει
    finally:
        conn.close()

def search_ioannina():
    print("🏠 Ξεκινάει η αναζήτηση στα Ιωάννινα...")
    
    # Παράδειγμα URL αναζήτησης (Σπίτια & Καταστήματα, έως 40k)
    # Σημείωση: Στο μέλλον θα προσθέσουμε περισσότερα URLs από Xe.gr κλπ.
    search_url = "https://www.spitogatos.gr/pwliseis-akinitwn/ioannina/timi-ews-40000"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    # Εδώ θα γινόταν το κανονικό scraping. Για το τεστ, προσομοιώνουμε ένα εύρημα:
    results = [
        {
            "title": "Ισόγειο Κατάστημα στο Κέντρο",
            "price": 35000,
            "sq_meters": 45,
            "floor": "Ισόγειο",
            "year_built": 1995,
            "location": "Κέντρο, Ιωάννινα",
            "type": "Κατάστημα",
            "url": "https://www.spitogatos.gr/aggelia/123456"
        }
    ]

    for item in results:
        item['price_per_sqm'] = item['price'] / item['sq_meters']
        
        # Φίλτρο: Ισόγειο ή πάνω και τιμή <= 40000
        if item['price'] <= 40000 and "Υπόγειο" not in item['floor']:
            is_new = save_to_db(item)
            if is_new:
                msg = f"📍 **Νέο Ακίνητο στα Ιωάννινα!**\n💰 Τιμή: {item['price']}€\n📐 Τ.Μ.: {item['sq_meters']}\n🏢 Όροφος: {item['floor']}\n🏗️ Έτος: {item['year_built']}\n🔗 {item['url']}"
                notify_discord_re(WEBHOOK_IOANNINA, msg)
                print(f"✅ Βρέθηκε και στάλθηκε: {item['title']}")
            else:
                print(f"⏭️ Το ακίνητο {item['url']} υπάρχει ήδη στη βάση.")

if __name__ == "__main__":
    search_ioannina()
