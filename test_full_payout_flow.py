import os, time
from hunter import process_task
from markets_extension import scan_algora, scan_gitcoin
from dotenv import load_dotenv

load_dotenv('/root/agent_system/.env')
WALLET = os.getenv('PAYMENT_WALLET', 'C4PcQjqDW4a5Pvhx5ZFPvAodkGiVG49q8dMvpskqSvuH')

def run_payout_test():
    print(f"💰 Έναρξη Test Πληρωμών για το Wallet: {WALLET}")
    
    simulated_tasks = [
        {
            "market": "Bountycaster (Farcaster)",
            "title": "Python script for Daily Crypto Reports",
            "desc": "Need a script that sends daily BTC/ETH prices to Discord.",
            "link": "https://bountycaster.xyz/test-1",
            "id": "fc_001"
        },
        {
            "market": "Algora (GitHub Native)",
            "title": "Fix bug in React Navbar",
            "desc": "The mobile menu does not close on click. PR needed.",
            "link": "https://github.com/algora-io/test-2",
            "id": "algora_002"
        },
        {
            "market": "Gitcoin (RSS/Feed)",
            "title": "Smart Contract Audit for DEX",
            "desc": "Review the liquidity pool contract for reentrancy.",
            "link": "https://gitcoin.co/test-3",
            "id": "gitcoin_003"
        }
    ]

    for task in simulated_tasks:
        print(f"\n🚀 Δοκιμή Αγοράς: {task['market']}")
        # Εδώ καλούμε την process_task με το wallet address ως μέρος του prompt
        instruction = f"Solve this and ensure the wallet {WALLET} is in the code comments for payment."
        process_task(task['market'], task['title'], f"{task['desc']} | {instruction}", task['link'], task['id'])
        print(f"✅ Η λύση για {task['market']} υποβλήθηκε.")
        time.sleep(5)

    print("\n🏁 Το Test ολοκληρώθηκε. Έλεγξε το GitHub για τα νέα αρχεία sol_*.py και το Discord για τα confirmations.")

if __name__ == "__main__":
    run_payout_test()
