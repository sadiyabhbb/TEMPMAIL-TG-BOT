import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8035083791:AAF9m2iDWqhqi4UGoHn5EP1_z3znpRSdsa4"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Temp Email পেতে /check দিন।")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
        email = response.json()[0]
        await update.message.reply_text(f"🧪 আপনার টেম্প ইমেইল:\n`{email}`", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("❌ ইমেইল আনতে সমস্যা হয়েছে।")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.run_polling()
