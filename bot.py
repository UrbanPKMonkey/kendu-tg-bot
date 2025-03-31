import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAILWAY_URL = os.getenv("RAILWAY_URL")
PORT = int(os.environ.get("PORT", "80"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ /start triggered")
    await update.message.reply_text("👋 Hello! This is your debug webhook bot.")

async def log_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"📥 Raw update received: {update}")

def main():
    if not BOT_TOKEN or not RAILWAY_URL:
        print("❌ Missing BOT_TOKEN or RAILWAY_URL")
        exit(1)

    full_webhook_url = f"https://{RAILWAY_URL.replace('https://', '').replace('http://', '')}/webhook"
    print(f"🌐 Webhook set to: {full_webhook_url}")

    app = Application.builder().token(BOT_TOKEN).build()

    # Basic command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, log_all))

    async def setup(application):
        await application.bot.set_webhook(url=full_webhook_url)
        print("✅ Webhook registered with Telegram")

    app.post_init = setup

    print("🚀 Starting webhook listener...")
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=full_webhook_url
    )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"🔥 Fatal error: {e}")
