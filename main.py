import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Bot Telegram aktif 🚀")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Dummy data (nanti bisa diganti dengan data API)
    entry = "60,500 USDT"
    tp = "63,000 USDT"
    sl = "59,000 USDT"
    rsi = "42.7 (Netral)"
    macd = "Bullish crossover"
    ema_21 = "60,200"
    ma_50 = "59,800"
    tvl = "$5.2B"
    fdv = "$1.2T"
    whale = "🔼 Positif"
    rekomendasi = "✅ BUY"

    message = f"""📢 [SINYAL TRADING] BTC/USDT

✅ Entry: {entry}
🎯 TP: {tp}
⛔ SL: {sl}

📊 RSI: {rsi}
📈 MACD: {macd}
📉 EMA 21: {ema_21}
📏 MA 50: {ma_50}

💰 TVL: {tvl}
🏦 FDV: {fdv}

🐋 Akumulasi Whale: {whale}
🛒 Rekomendasi: {rekomendasi}

#CryptoSignal #BTC #TradingBot
"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    print("Bot berjalan di Railway...")
    app.run_polling()
