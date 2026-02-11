import os, time
from hunter import process_task
from dotenv import load_dotenv

load_dotenv('/root/agent_system/.env')

def run_stress_test():
    print("🔥 Ξεκινάω STRESS TEST: Προσομοίωση 3 ταυτόχρονων Bounties...")
    
    test_tasks = [
        {
            "source": "Stress_Test_1",
            "title": "Build a Rust CLI tool for file encryption",
            "desc": "Create a tool that uses AES-256-GCM to encrypt local files. Fast and secure.",
            "link": "https://bounties.example/rust-1",
            "hash": "0xSTRESS1"
        },
        {
            "source": "Stress_Test_2",
            "title": "React Dashboard for Crypto Tracking",
            "desc": "Simple React dashboard using Tailwind CSS to display live prices from CoinGecko API.",
            "link": "https://bounties.example/react-2",
            "hash": "0xSTRESS2"
        },
        {
            "source": "Stress_Test_3",
            "title": "Smart Contract Auditor Script in Solidity",
            "desc": "A python script that scans Solidity files for reentrancy vulnerabilities.",
            "link": "https://bounties.example/solidity-3",
            "hash": "0xSTRESS3"
        }
    ]

    for i, task in enumerate(test_tasks, 1):
        print(f"\n🚀 Επεξεργασία Task {i}/3: {task['title']}")
        process_task(task['source'], task['title'], task['desc'], task['link'], task['hash'])
        print(f"⏳ Αναμονή 10 δευτερολέπτων για το επόμενο...")
        time.sleep(10)

if __name__ == "__main__":
    run_stress_test()
