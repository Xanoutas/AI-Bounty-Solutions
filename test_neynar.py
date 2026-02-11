import os, requests
from dotenv import load_dotenv

load_dotenv('/root/agent_system/.env')

NEYNAR_API_KEY = os.getenv("NEYNAR_API_KEY")
SIGNER_UUID = os.getenv("SIGNER_UUID")
DISCORD_URL = "https://discord.com/api/webhooks/1469793300075512090/dCdj2wFQuDrw597CmZ_nTcSzlleVxTL6zHkzYhXYfia3oneI0Ua0mrfxI0y5K7v14bUW"

def test_neynar():
    url = "https://api.neynar.com/v2/farcaster/cast"
    headers = {
        "api_key": NEYNAR_API_KEY,
        "content-type": "application/json"
    }
    payload = {
        "signer_uuid": SIGNER_UUID,
        "text": "🛠️ EPYC Hunter V13.0: Connectivity Test Successful. I am ready to submit bounties. 🚀"
    }
    
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        if r.status_code == 200:
            msg = "✅ **Neynar Test Success!** Ο Agent μπορεί να ποστάρει στο Farcaster."
        else:
            msg = f"❌ **Neynar Test Failed!** Status: {r.status_code}, Error: {r.text}"
    except Exception as e:
        msg = f"⚠️ **Neynar Connection Error:** {str(e)}"
    
    requests.post(DISCORD_URL, json={"content": msg})
    print(msg)

if __name__ == "__main__":
    test_neynar()
