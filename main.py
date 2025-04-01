import os
from contextlib import asynccontextmanager
from http import HTTPStatus
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from telegram import Update, BotCommand, MenuButtonCommands
from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler
)

# 🔌 Command and Callback Logic
from handlers.commands import (
    start, menu, about, eco, buykendu, contracts, faq, follow,
    logout, restart  # ✅ Registered reset logic
)
from handlers.callbacks import handle_button

# 🔐 Load environment variables
load_dotenv()
BOT_TOKEN: str = os.getenv('BOT_TOKEN')
RAILWAY_URL: str = os.getenv('RAILWAY_PUBLIC_DOMAIN')

# ⚙️ Build the Telegram bot application
bot_app = (
    Application.builder()
    .token(BOT_TOKEN)
    .updater(None)
    .build()
)

# 🛠 Post-start setup: Slash commands + webhook
async def post_init(application):
    print("🛠 Setting up slash commands and webhook menu...")

    commands = [
        BotCommand("menu", "Open the main Kendu Menu"),
        BotCommand("about", "Learn about Kendu"),
        BotCommand("eco", "Explore the Ecosystem"),
        BotCommand("buykendu", "How to Buy Kendu"),
        BotCommand("contracts", "View Contract Addresses"),
        BotCommand("faq", "Frequently Asked Questions"),
        BotCommand("follow", "Official Links & Socials"),
        BotCommand("logout", "Clear menu state and reset"),        # ✅
        BotCommand("restart", "Full reset & reinit the bot")       # ✅
    ]

    await application.bot.set_my_commands(commands)
    await application.bot.set_chat_menu_button(menu_button=MenuButtonCommands())

    webhook_url = f"https://{RAILWAY_URL}/"
    await application.bot.setWebhook(url=webhook_url)
    print(f"🌐 Webhook registered at: {webhook_url}")

# 🔁 Telegram lifecycle with graceful start/stop
@asynccontextmanager
async def lifespan(_: FastAPI):
    async with bot_app:
        await bot_app.start()
        print("✅ Bot started.")
        yield
        await bot_app.stop()
        print("🛑 Bot stopped.")

# 🚀 FastAPI app with Telegram webhook
app = FastAPI(lifespan=lifespan)

@app.post("/")
async def process_update(request: Request):
    message = await request.json()
    update = Update.de_json(data=message, bot=bot_app.bot)
    await bot_app.process_update(update)
    return Response(status_code=HTTPStatus.OK)

# ✅ Slash Commands
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("menu", menu))
bot_app.add_handler(CommandHandler("about", about))
bot_app.add_handler(CommandHandler("eco", eco))
bot_app.add_handler(CommandHandler("buykendu", buykendu))
bot_app.add_handler(CommandHandler("contracts", contracts))
bot_app.add_handler(CommandHandler("faq", faq))
bot_app.add_handler(CommandHandler("follow", follow))
bot_app.add_handler(CommandHandler("logout", logout))     # ✅
bot_app.add_handler(CommandHandler("restart", restart))   # ✅

# 🔘 Inline Button Callbacks
bot_app.add_handler(CallbackQueryHandler(handle_button))

# 🔧 Attach post-init setup
bot_app.post_init = post_init
