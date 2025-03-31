import os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import BotCommand, MenuButtonCommands
from handlers.commands import start, menu, about, eco, buykendu, contracts, faq, follow
from handlers.callbacks import handle_button

# 🔐 Load your bot token and Railway-provided URL
BOT_TOKEN = os.getenv("BOT_TOKEN")
RAILWAY_URL = os.getenv("RAILWAY_URL")  # Set this in Railway variables

# 🔘 Register slash commands, menu, and webhook URL
async def set_bot_commands(application):
    commands = [
        BotCommand("menu", "Open the main Kendu Menu"),
        BotCommand("about", "Learn about Kendu"),
        BotCommand("eco", "Explore the Ecosystem"),
        BotCommand("buykendu", "How to Buy Kendu"),
        BotCommand("contracts", "View Contract Addresses"),
        BotCommand("faq", "Frequently Asked Questions"),
        BotCommand("follow", "Official Links & Socials"),
    ]
    await application.bot.set_my_commands(commands)
    await application.bot.set_chat_menu_button(menu_button=MenuButtonCommands())

    # ✅ Explicitly set the webhook
    webhook_url = RAILWAY_URL + "/webhook"
    await application.bot.set_webhook(url=webhook_url)

# 🚀 Main Entry Point
def main():
    print("🔧 bot.py: main() starting...")

    if os.getenv("FORCE_EXIT") == "true":
        print("🛑 FORCE_EXIT enabled. Shutting down immediately.")
        exit(0)

    if not BOT_TOKEN or not RAILWAY_URL:
        print("❌ BOT_TOKEN or RAILWAY_URL missing. Exiting.")
        exit(1)

    print("🔐 BOT_TOKEN & RAILWAY_URL loaded.")

    app = Application.builder().token(BOT_TOKEN).build()
    print("✅ Application built.")

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("eco", eco))
    app.add_handler(CommandHandler("buykendu", buykendu))
    app.add_handler(CommandHandler("contracts", contracts))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(CommandHandler("follow", follow))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.post_init = set_bot_commands
    print("✅ Handlers registered.")

    # 🟢 Start webhook server
    print("🚀 Starting webhook server...")
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", "8080")),
        webhook_url=f"{RAILWAY_URL}/webhook"
    )

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"🔥 Error during bot startup: {e}")
