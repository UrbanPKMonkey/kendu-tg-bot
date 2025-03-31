import os
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAILWAY_URL = os.getenv("RAILWAY_URL")

async def echo_everything(update, context: ContextTypes.DEFAULT_TYPE):
    print("📨 Telegram sent something!")
    print(update)

def main():
    if not BOT_TOKEN or not RAILWAY_URL:
        print("❌ Missing BOT_TOKEN or RAILWAY_URL")
        return

    full_url = f"https://{RAILWAY_URL.replace('https://', '').replace('http://', '')}/webhook"
    print(f"🌐 Setting webhook: {full_url}")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, echo_everything))

    async def setup(application):
        await application.bot.set_webhook(url=full_url)
        print("✅ Webhook registered with Telegram")

    app.post_init = setup

    print("🚀 Starting webhook listener...")
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", "80")),
        webhook_url=full_url
    )


if __name__ == "__main__":
    main()
