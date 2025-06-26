from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

BOT_TOKEN = "8035083791:AAF9m2iDWqhqi4UGoHn5EP1_z3znpRSdsa4"

user_emails = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    try:
        response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
        email = response.json()[0]
        user_emails[user_id] = email
        await update.message.reply_text(f"✅ তোমার টেম্প ইমেইল:\n`{email}`", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text("⚠️ টেম্প ইমেইল আনতে সমস্যা হয়েছে।")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    email = user_emails.get(user_id)

    if not email:
        await update.message.reply_text("⚠️ আগে /start দিয়ে টেম্প ইমেইল নাও।")
        return

    login, domain = email.split('@')
    try:
        url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
        messages = requests.get(url).json()

        if not messages:
            await update.message.reply_text("📭 এখনো কোনো ইমেইল পাওয়া যায়নি।")
        else:
            msg = messages[0]
            subject = msg.get("subject", "No subject")
            from_mail = msg.get("from", "Unknown sender")
            await update.message.reply_text(f"📩 ইমেইল এসেছে:\n🧾 Subject: {subject}\n👤 From: {from_mail}")
    except Exception as e:
        await update.message.reply_text("⚠️ ইমেইল চেক করতে সমস্যা হয়েছে।")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))

    app.run_polling()
