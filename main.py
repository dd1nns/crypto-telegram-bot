import os
import csv
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Logging fungsi
def log_signal(symbol, price, recommendation, rsi, macd, tp, sl, whale_activity):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    row = [timestamp, symbol, price, recommendation, rsi, macd, tp, sl, whale_activity]

    with open('logs.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Bot Telegram crypto aktif 🚀\nKetik /btc atau /eth untuk mulai.")

# Command: /signal manual
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=CHAT_ID, text="📈 Sinyal crypto terkirim!")

# Fungsi utama coin
async def handle_coin(update: Update, context: ContextTypes.DEFAULT_TYPE, symbol: str):
    # Data dummy — nanti diganti dari API real-time
    coin_data = {
        "BTC": 65800,
        "ETH": 3450,
        "XRP": 0.63,
        "SOL": 178.3,
        "DOGE": 0.12,
        "SUI": 0.85,
        "SEI": 0.38,
        "BNB": 525.1
    }

    price = coin_data.get(symbol.upper(), 1.0)
    rsi = 41.3
    macd_signal = "MACD Bullish"
    recommendation = "BUY" if rsi < 50 else "WAIT"
    tp = round(price * 1.03, 4)
    sl = round(price * 0.97, 4)
    whale_status = "Accumulating"

    message = f"""
📊 Sinyal {symbol.upper()}
Harga: ${price}
Rekomendasi: {recommendation}
RSI: {rsi}
MACD: {macd_signal}
TP: ${tp}
SL: ${sl}
Whale: {whale_status}
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    log_signal(symbol.upper(), price, recommendation, rsi, macd_signal, tp, sl, whale_status)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handler dasar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    # Coin handlers
    coin_list = ["btc", "eth", "xrp", "sol", "doge", "sui", "sei", "bnb"]
    for coin in coin_list:
        app.add_handler(CommandHandler(coin, lambda u, c, coin=coin: handle_coin(u, c, coin.upper())))

    print("Bot berjalan... 🚀")
    app.run_polling()
