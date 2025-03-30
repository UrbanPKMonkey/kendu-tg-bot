from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import BotCommand, MenuButtonCommands
from handlers.commands import start, menu, about, eco, buykendu, contracts, faq, follow
from handlers.callbacks import handle_button
import os

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
    app = Application.builder().token(BOT_TOKEN).build()

    # ✅ Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("eco", eco))
    app.add_handler(CommandHandler("buykendu", buykendu))
    app.add_handler(CommandHandler("contracts", contracts))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(CommandHandler("follow", follow))

    # ✅ Register callback query handler for button presses
    app.add_handler(CallbackQueryHandler(handle_button))

    # ✅ Set slash commands & menu after bot starts
    app.post_init = set_bot_commands

    # 🟢 Start polling
    app.run_polling()


if __name__ == "__main__":
    main()
