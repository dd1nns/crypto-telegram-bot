import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

COIN_LIST = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
    "xrp": "ripple",
    "doge": "dogecoin"
}

def fetch_coin_data(symbol):
    coin_id = COIN_LIST.get(symbol)
    if not coin_id:
        return None

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        price_res = requests.get(url).json()
        price = price_res[coin_id]["usd"]
    except:
        return None

    # Dummy indikator (buat sederhana dulu)
    rsi = 55
    macd = "Bullish"
    ema21 = price * 0.98
    ma50 = price * 1.01
    whale = "High" if symbol == "btc" else "Low"

    recommendation = "BUY" if rsi < 70 and macd == "Bullish" and whale == "High" else "WAIT"

    return {
        "price": price,
        "rsi": rsi,
        "macd": macd,
        "ema21": ema21,
        "ma50": ma50,
        "whale": whale,
        "tp": price * 1.03,
        "sl": price * 0.97,
        "entry": price * 0.99,
        "recommendation": recommendation
    }

async def coin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = update.message.text.replace("/", "").lower()
    data = fetch_coin_data(symbol)

    if not data:
        await update.message.reply_text("⚠️ Coin tidak dikenali.")
        return

    msg = (
        f"💰 {symbol.upper()} Price: ${data['price']:,}\n"
        f"📥 Entry: ${data['entry']:.2f}\n"
        f"🎯 TP: ${data['tp']:.2f} | 🛡️ SL: ${data['sl']:.2f}\n\n"
        f"📊 RSI: {data['rsi']}\n"
        f"📈 MACD: {data['macd']}\n"
        f"📉 EMA21: ${data['ema21']:.2f} | MA50: ${data['ma50']:.2f}\n"
        f"🐳 Whale Accumulation: {data['whale']}\n"
        f"🧠 Rekomendasi: {data['recommendation']}"
    )
    await update.message.reply_text(msg)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Bot aktif!\nKetik /btc, /eth, /sol, dll untuk cek sinyal.")

# 🔁 Fungsi auto alert tiap 15 menit
async def send_auto_signals(app):
    for symbol in COIN_LIST:
        data = fetch_coin_data(symbol)
        if data:
            msg = (
                f"⏰ Auto Signal {symbol.upper()}\n"
                f"💰 Price: ${data['price']}\n"
                f"📥 Entry: ${data['entry']:.2f} | TP: ${data['tp']:.2f} | SL: ${data['sl']:.2f}\n"
                f"📊 RSI: {data['rsi']} | MACD: {data['macd']} | Whale: {data['whale']}\n"
                f"📈 EMA21: ${data['ema21']:.2f} | MA50: ${data['ma50']:.2f}\n"
                f"✅ Rekomendasi: {data['recommendation']}"
            )
            await app.bot.send_message(chat_id=CHAT_ID, text=msg)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command per coin
    for cmd in COIN_LIST:
        app.add_handler(CommandHandler(cmd, coin_command))

    app.add_handler(CommandHandler("start", start))

    # Scheduler auto sinyal tiap 15 menit
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: app.create_task(send_auto_signals(app)), 'interval', minutes=15)
    scheduler.start()

    print("🤖 Bot Telegram berjalan...")
    app.run_polling()
