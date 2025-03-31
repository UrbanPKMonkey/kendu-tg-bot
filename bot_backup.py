from telegram.ext import Application, MessageHandler, ContextTypes, filters
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAILWAY_URL = os.getenv("RAILWAY_URL")

async def echo(update, context: ContextTypes.DEFAULT_TYPE):
    print("📨 Telegram sent something!")
    await update.message.reply_text("👋 Bot received your message!")

def main():
    if not BOT_TOKEN or not RAILWAY_URL:
        print("❌ Missing BOT_TOKEN or RAILWAY_URL")
        return

    full_url = f"https://{RAILWAY_URL.replace('https://', '').replace('http://', '')}/webhook"
    print(f"🌐 Setting webhook: {full_url}")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, echo))

    async def setup(application):
        await application.bot.set_webhook(url=full_url)
        print("✅ Webhook registered with Telegram")

    app.post_init = setup

    print("🚀 Starting webhook listener...")

    # THIS is the line that keeps the container alive
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", "80")),
        webhook_url=full_url
    )

if __name__ == "__main__":
    main()