import os, requests
from dotenv import load_dotenv

load_dotenv('/root/agent_system/.env')

LOG_FILES = ['hunter.log', 'markets.log', 'monitor.log']
WEBHOOK = os.getenv('DISCORD_WEBHOOK')

def scan_logs():
    for log in LOG_FILES:
        path = f"/root/agent_system/{log}"
        if os.path.exists(path):
            with open(path, 'r') as f:
                lines = f.readlines()
                for line in lines[-20:]: # Έλεγχος των τελευταίων 20 γραμμών
                    if "Error" in line or "Exception" in line or "401" in line:
                        msg = f"⚠️ **EPYC ALERT**: Σφάλμα στο αρχείο {log}\n```{line.strip()}```"
                        requests.post(WEBHOOK, json={"content": msg})
                        return # Στέλνουμε ένα για να μην γίνει spam

if __name__ == "__main__":
    scan_logs()
