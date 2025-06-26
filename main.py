import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ✅ আপনার Bot Token এখানে
BOT_TOKEN = "8035083791:AAF9m2iDWqhqi4UGoHn5EP1_z3znpRSdsa4"

# ইউজারের ইমেইল সংরক্ষণের জন্য ডিকশনারি
user_data = {}

# /start কমান্ড: টেম্প ইমেইল তৈরি
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
        if res.status_code != 200:
            await update.message.reply_text("⚠️ ইমেইল আনতে সমস্যা হয়েছে, পরে আবার চেষ্টা করুন।")
            return

        data = res.json()
        if not data:
            await update.message.reply_text("⚠️ ইমেইল পাওয়া যায়নি, আবার চেষ্টা করুন।")
            return

        email = data[0]
        user_data[update.effective_chat.id] = email
        await update.message.reply_text(f"✅ আপনার টেম্প ইমেইল:\n`{email}`", parse_mode="MarkdownV2")
    except Exception as e:
        await update.message.reply_text("❌ টেম্প ইমেইল তৈরি করতে সমস্যা হচ্ছে।")
        print("START ERROR:", e)

# /check কমান্ড: ইনবক্স চেক করা
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
            text = "\n\n".join(
                [f"📧 From: {msg['from']}\n📝 Subject: {msg['subject']}" for msg in messages]
            )
            await update.message.reply_text(f"📥 আপনার ইনবক্স:\n\n{text}")
    except Exception as e:
        await update.message.reply_text("❌ চেক করতে সমস্যা হয়েছে।")
        print("CHECK ERROR:", e)

# Bot run করা
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.run_polling()
