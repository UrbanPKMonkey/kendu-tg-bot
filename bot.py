import os
from contextlib import asynccontextmanager
from http import HTTPStatus
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

# 🔐 Load environment variables
load_dotenv()
BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN')
RAILWAY_URL: str = os.getenv('RAILWAY_PUBLIC_DOMAIN')

# ⚒️ Build the Telegram Application
bot_app = (
    Application.builder()
    .token(BOT_TOKEN)
    .updater(None)
    .build()
)

# 🔁 Lifespan handler — registers webhook and starts bot lifecycle
@asynccontextmanager
async def lifespan(_: FastAPI):
    webhook_url = f"https://{RAILWAY_URL}/"
    print(f"🌐 Setting webhook: {webhook_url}")
    await bot_app.bot.setWebhook(url=webhook_url)

    async with bot_app:
        await bot_app.start()
        print("✅ Bot started with webhook.")
        yield
        await bot_app.stop()
        print("🛑 Bot stopped.")

# 🚀 FastAPI app setup
app = FastAPI(lifespan=lifespan)

# 📥 Webhook endpoint
@app.post("/")
async def process_update(request: Request):
    message = await request.json()
    update = Update.de_json(data=message, bot=bot_app.bot)
    await bot_app.process_update(update)
    return Response(status_code=HTTPStatus.OK)

# ✅ Echo handler (replaces /start or text replies)
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📨 Telegram sent something!")
    if update.message:
        await update.message.reply_text("👋 Bot received your message!")

# 📦 Register handlers
bot_app.add_handler(MessageHandler(filters.ALL, echo))
