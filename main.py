import os
from contextlib import asynccontextmanager
from http import HTTPStatus
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from telegram import Update, BotCommand, MenuButtonCommands
from telegram.ext import Application, CallbackQueryHandler
import asyncio  # ✅ Needed for background tasks

# 🔧 Routing Logic
from handlers.router_commands import register_slash_commands, COMMAND_DEFINITIONS
from handlers.router_callbacks import handle_button, handle_show_commands

# ✅ Buy Watchers (ETH, BASE, SOL)
from watchers.watcher_eth import run_eth_buy_watcher
from watchers.watcher_base import run_base_buy_watcher
from watchers.watcher_sol import run_sol_buy_watcher

# 🌱 Load environment variables
load_dotenv()
BOT_TOKEN: str = os.getenv('BOT_TOKEN')
RAILWAY_URL: str = os.getenv('RAILWAY_PUBLIC_DOMAIN')

# ❗ Validate required env vars
if not BOT_TOKEN or not RAILWAY_URL:
    raise ValueError("Missing BOT_TOKEN or RAILWAY_PUBLIC_DOMAIN in .env")

# 🤖 Build the Telegram bot app
bot_app = Application.builder().token(BOT_TOKEN).updater(None).build()

# 🛠️ Post-init: setup webhook + dynamic slash commands
async def post_init(application):
    print("🛠️ Setting up webhook + commands...")

    # 🔄 Dynamic command suggestions (blue menu)
    commands = [BotCommand(cmd, desc) for cmd, desc in COMMAND_DEFINITIONS]
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

        # 🚀 Launch Buy Watchers in background
        print("🚀 Launching ETH Buy Watcher...")
        asyncio.create_task(run_eth_buy_watcher(bot_app.bot))

        print("🚀 Launching BASE Buy Watcher...")
        asyncio.create_task(run_base_buy_watcher(bot_app.bot))

        print("🚀 Launching SOL Buy Watcher...")
        asyncio.create_task(run_sol_buy_watcher(bot_app.bot))

        print("✅ Buy Watchers Launched!")  # ✅ Confirmation
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
