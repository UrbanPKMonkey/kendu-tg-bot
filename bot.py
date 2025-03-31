import os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import BotCommand, MenuButtonCommands
from handlers.commands import start, menu, about, eco, buykendu, contracts, faq, follow
from handlers.callbacks import handle_button

# 🔐 Load your bot token from env
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🔘 Register slash commands & blue menu button
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

# 🚀 Main Entry Point
def main():
    print("🔧 bot.py: main() starting...")

    # ✅ Check for FORCE_EXIT (for safe Railway shutdowns)
    if os.getenv("FORCE_EXIT") == "true":
        print("🛑 FORCE_EXIT enabled. Shutting down immediately.")
        exit(0)

    # ✅ Confirm BOT_TOKEN loaded
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found in environment! Exiting.")
        exit(1)
    else:
        print("🔐 BOT_TOKEN found.")

    # ✅ Build the Telegram application
    app = Application.builder().token(BOT_TOKEN).build()
    print("✅ Application built.")

    # ✅ Register slash command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("eco", eco))
    app.add_handler(CommandHandler("buykendu", buykendu))
    app.add_handler(CommandHandler("contracts", contracts))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(CommandHandler("follow", follow))
    print("✅ Command handlers registered.")

    # ✅ Register callback query handler for buttons
    app.add_handler(CallbackQueryHandler(handle_button))
    print("✅ Callback handlers registered.")

    # ✅ Set bot commands and menu button
    app.post_init = set_bot_commands

    # 🟢 Start polling
    print("🚀 Starting polling...")
    app.run_polling()

# 🧯 Crash Protection
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"🔥 Error during bot startup: {e}")
