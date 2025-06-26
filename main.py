import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes
)

# Load .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Dictionary to store user emails
user_data = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")

        # Check if response is OK
        if res.status_code != 200:
            await update.message.reply_text("⚠️ ইমেইল আনতে সমস্যা হচ্ছে। পরে চেষ্টা করুন।")
            return

        data = res.json()

        # Check if list is not empty
        if not data:
            await update.message.reply_text("⚠️ ইমেইল লিস্ট ফাঁকা।")
            return

        email = data[0]
        user_id = update.effective_chat.id
        user_data[user_id] = email

        await update.message.reply_text(f"✅ আপনার টেম্প ইমেইল:\n`{email}`", parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text("❌ টেম্প ইমেইল তৈরি করতে সমস্যা হচ্ছে।")
        print("START ERROR:", e)


# Check command
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_chat.id
        email = user_data.get(user_id)

        if not email:
            await update.message.reply_text("⚠️ আগে /start দিন টেম্প ইমেইল পেতে।")
            return

        login, domain = email.split('@')
        url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
        res = requests.get(url)

        if res.status_code != 200:
            await update.message.reply_text("⚠️ মেইল চেক করতে সমস্যা হচ্ছে।")
            return

        messages = res.json()

        if not messages:
            await update.message.reply_text("📭 এখনো কোনো মেইল আসেনি।")
        else:
            msg_list = "\n\n".join(
                [f"📧 From: {msg['from']}\n📨 Subject: {msg['subject']}" for msg in messages]
            )
            await update.message.reply_text(f"📥 ইনবক্স:\n\n{msg_list}")

    except Exception as e:
        await update.message.reply_text("❌ চেক করতে সমস্যা হয়েছে।")
        print("CHECK ERROR:", e)


if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))

    app.run_polling()
