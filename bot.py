from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from handlers.commands import start, menu
from handlers.callbacks import handle_button
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))

    # Callback Handlers
    app.add_handler(CallbackQueryHandler(handle_button))

    app.run_polling()

if __name__ == "__main__":
    main()
