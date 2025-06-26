import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    res = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
    email = res.json()[0]
    context.user_data['email'] = email
    await update.message.reply_text(f"✅ আপনার টেম্প ইমেইল: {email}\n\n👉 এখন /check দিয়ে ইনবক্স দেখতে পারেন।")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'email' not in context.user_data:
        await update.message.reply_text("⚠️ আগে /start দিন টেম্প ইমেইল পেতে।")
        return

    email = context.user_data['email']
    login, domain = email.split('@')
    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
    mails = requests.get(url).json()

    if not mails:
        await update.message.reply_text("📭 এখনো কোনো মেইল আসেনি।")
        return

    msg = ""
    for mail in mails:
        msg += f"📩 From: {mail['from']}\nSubject: {mail['subject']}\n\n"

    await update.message.reply_text(msg)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.run_polling()

if __name__ == "__main__":
    main()
