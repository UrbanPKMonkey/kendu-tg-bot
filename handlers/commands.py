from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Hello! Welcome to the bot. Use /menu to get started.")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛍 Shop Merch", callback_data="shop_merch"),
         InlineKeyboardButton("💰 Buy Crypto", callback_data="buy_crypto")],
        [InlineKeyboardButton("📜 View History", callback_data="view_history"),
         InlineKeyboardButton("🔗 Social Links", callback_data="social_links")]
    ]

    await update.message.reply_text(
        "🛠️ What would you like to do?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
