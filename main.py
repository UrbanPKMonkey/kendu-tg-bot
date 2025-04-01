import os
from contextlib import asynccontextmanager
from http import HTTPStatus
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from telegram import Update, BotCommand, MenuButtonCommands
from telegram.ext import Application, CallbackQueryHandler

# 🔧 Routing Logic
from handlers.router_commands import register_slash_commands
from handlers.router_callbacks import handle_button, handle_show_commands

# 🌱 Load environment variables
load_dotenv()
BOT_TOKEN: str = os.getenv('BOT_TOKEN')
RAILWAY_URL: str = os.getenv('RAILWAY_PUBLIC_DOMAIN')

# ❗ Validate required env vars
if not BOT_TOKEN or not RAILWAY_URL:
    raise ValueError("Missing BOT_TOKEN or RAILWAY_PUBLIC_DOMAIN in .env")

# 🤖 Build the Telegram bot app
bot_app = Application.builder().token(BOT_TOKEN).updater(None).build()

# 🛠️ Post-init: setup webhook + slash commands
async def post_init(application):
    print("🛠️ Setting up webhook + commands...")

    commands = [
        BotCommand("start", "Start the bot and get the welcome screen"),
        BotCommand("menu", "Open the main menu"),
        BotCommand("about", "Learn about Kendu"),
        BotCommand("eco", "Explore the Ecosystem"),
        BotCommand("buykendu", "How to Buy Kendu"),
        BotCommand("contracts", "View Contract Addresses"),
        BotCommand("faq", "Questions & Answers"),
        BotCommand("follow", "Official Links & Socials"),
        BotCommand("logout", "Clear menu state and reset"),
        BotCommand("restart", "Full reset & reinit the bot")
    ]
    await application.bot.set_my_commands(commands)
    await application.bot.set_chat_menu_button(menu_button=MenuButtonCommands())

    webhook_url = f"https://{RAILWAY_URL}/"
    try:
        await application.bot.setWebhook(url=webhook_url)
        print(f"🌐 Webhook set to: {webhook_url}")
    except Exception as e:
        print(f"⚠️ Failed to set webhook: {e}")

# 🔁 Lifecycle hook for FastAPI
@asynccontextmanager
async def lifespan(_: FastAPI):
    async with bot_app:
        await bot_app.start()
        print("✅ Bot started")
        yield
        await bot_app.stop()
        print("🛑 Bot stopped")

# 🚀 Create FastAPI app with lifecycle
app = FastAPI(lifespan=lifespan)

@app.post("/")
async def process_update(request: Request):
    data = await request.json()
    update = Update.de_json(data=data, bot=bot_app.bot)
    await bot_app.process_update(update)
    return Response(status_code=HTTPStatus.OK)

# 🧠 Register all slash commands
register_slash_commands(bot_app)

# 🔘 Register callback handlers
bot_app.add_handler(CallbackQueryHandler(handle_button))
bot_app.add_handler(CallbackQueryHandler(handle_show_commands, pattern="^show_commands$"))

# ✅ Hook post-init
bot_app.post_init = post_init
