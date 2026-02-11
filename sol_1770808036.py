import requests
import discord
import asyncio

# Configuration variables
DISCORD_WEBHOOK_URL = 'YOUR_DISCORD_WEBHOOK_URL'  # Replace with your webhook URL
COIN_API_URL = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd'

# Function to get BTC and ETH prices
async def get_crypto_prices():
    response = requests.get(COIN_API_URL)
    data = response.json()
    btc_price = data['bitcoin']['usd']
    eth_price = data['ethereum']['usd']
    return btc_price, eth_price

# Function to send a message to Discord
async def send_discord_message(message):
    webhook = discord.Webhook.from_url(DISCORD_WEBHOOK_URL, adapter=discord.RequestsWebhookAdapter())
    await webhook.send(content=message)

# Main function to fetch prices and send the report
async def daily_crypto_report():
    btc_price, eth_price = await get_crypto_prices()
    message = f"Daily Crypto Report:\nBitcoin (BTC): ${btc_price}\nEthereum (ETH): ${eth_price}"
    await send_discord_message(message)

# Run the main function as an event loop
if __name__ == '__main__':
    asyncio.run(daily_crypto_report())

# Wallet for payment: C4PcQjqDW4a5Pvhx5ZFPvAodkGiVG49q8dMvpskqSvuH


**Important Notes**:
1. Replace `'YOUR_DISCORD_WEBHOOK_URL'` with your actual Discord webhook URL.
2. This script uses the Coingecko API for free access to cryptocurrency prices.
3. Ensure Python environment has `discord.py` library installed (`pip install discord.py`).