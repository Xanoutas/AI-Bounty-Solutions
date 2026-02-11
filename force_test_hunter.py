import os, requests, subprocess
from hunter import process_task, auditor_solve_loop
from dotenv import load_dotenv

load_dotenv('/root/agent_system/.env')

def run_manual_test():
    print("🚀 Ξεκινάω Force Test για τον Hunter V14.0...")
    
    # Εικονικό Bounty για Python Automation (που σίγουρα θα πιάσει ο EPYC)
    test_title = "URGENT: Python script for automated server health monitoring"
    test_desc = "Create a python script that checks CPU and RAM usage and sends an alert if it exceeds 90%. Use ISO standards for logging."
    test_link = "https://example.com/test-bounty-123"
    test_hash = "0x1234567890abcdef1234567890abcdef12345678" # Mock hash για Farcaster

    print(f"🔍 Δοκιμή επεξεργασίας: {test_title}")
    
    # Καλούμε απευθείας τη συνάρτηση επεξεργασίας
    # Σημείωση: Το process_task θα ελέγξει αν το 'python' είναι στα keywords. 
    # Αν όχι, θα το προσθέσουμε προσωρινά για το τεστ.
    process_task("Manual_Test", test_title, test_desc, test_link, test_hash)

if __name__ == "__main__":
    run_manual_test()
