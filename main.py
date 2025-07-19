import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Contoh dummy URL API harga (bisa pakai CoinGecko, CMC, dll)
def get_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data.get(symbol, {}).get("usd", "N/A")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📡 Bot siap! Kirim /btc, /eth, /sol untuk cek harga.")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Sinyal harian akan ditambahkan nanti!")

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_price("bitcoin")
    await update.message.reply_text(f"₿ BTC/USD: ${price:,}\nEntry: ${price * 0.99:.2f}\nTP: ${price * 1.03:.2f}\nSL: ${price * 0.97:.2f}\n📊 RSI: 51\n🔁 MACD: Bullish\n📥 Whale Accumulation: High\n✅ Rekomendasi: BUY")

async def eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_price("ethereum")
    await update.message.reply_text(f"Ξ ETH/USD: ${price:,}\nEntry: ${price * 0.99:.2f}\nTP: ${price * 1.03:.2f}\nSL: ${price * 0.97:.2f}\n📊 RSI: 48\n🔁 MACD: Bearish\n📥 Whale Accumulation: Medium\n⚠️ Rekomendasi: WAIT")

async def sol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_price("solana")
    await update.message.reply_text(f"⚡ SOL/USD: ${price:,}\nEntry: ${price * 0.99:.2f}\nTP: ${price * 1.05:.2f}\nSL: ${price * 0.95:.2f}\n📊 RSI: 62\n🔁 MACD: Bullish\n📥 Whale Accumulation: Low\n✅ Rekomendasi: BUY")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("eth", eth))
    app.add_handler(CommandHandler("sol", sol))

    print("🚀 Bot berjalan...")
    app.run_polling()
