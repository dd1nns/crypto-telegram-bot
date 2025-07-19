import os
import time
import requests
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

def get_btc_price():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        data = response.json()
        return data["bitcoin"]["usd"]
    except Exception as e:
        return f"Error: {e}"

def send_signal():
    price = get_btc_price()
    message = f"🚨 BTC Signal\nHarga saat ini: ${price}"
    bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == "__main__":
    while True:
        send_signal()
        time.sleep(900)  # 15 menit
