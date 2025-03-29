from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context):
    await update.message.reply_text(
        "🧠 Welcome to the Official Kendu Bot — your all-in-one portal to the decentralized Kendu ecosystem.\n\n"
        "We don’t gamble, we work. 💪\n\n"
        "Explore the projects, get involved, and join the movement.\n\n"
        "📡 Available on Ethereum, Solana, and Base blockchains  \n"
        "✅ CertiK audit completed — verified & secured\n\n"
        "﹎﹎﹎﹎﹎﹎﹎\n"
        "🧭 Tap /menu to get started or explore:\n\n"
        "/about        → What is Kendu?  \n"
        "/eco          → Our Ecosystem  \n"
        "/buykendu     → How to Buy  \n"
        "/faq          → Questions & Answers  \n"
        "/contracts    → Contract Addresses  \n"
        "/follow       → Links & Socials  \n"
        "﹎﹎﹎﹎﹎﹎﹎\n\n"
        "📢 Official Website: https://kendu.io  \n"
        "🧵 Twitter/X: https://x.com/KenduInu  \n"
        "📰 Reddit: https://www.reddit.com/r/KenduInu_Ecosystem  \n\n"
        "Made with ❤️ by the Kendu Community."
    )

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
