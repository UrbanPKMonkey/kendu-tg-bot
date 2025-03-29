from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("🧠 About", callback_data="about")],
        [InlineKeyboardButton("🌐 Ecosystem", callback_data="ecosystem")],
        [InlineKeyboardButton("💰 Buy Kendu", callback_data="buy_kendu")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("🧾 Contract Addresses", callback_data="contract_addresses")],
        [InlineKeyboardButton("📄 Whitepaper", callback_data="whitepaper")],
        [InlineKeyboardButton("🔗 Follow", callback_data="follow_links")],
        [InlineKeyboardButton("📊 Market Info", callback_data="market_info")],
        [InlineKeyboardButton("🔐 Security Status", callback_data="security")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🧠 Welcome to the Official Kendu Bot — your all-in-one portal to the decentralized Kendu ecosystem.\n\n"
        "We don’t gamble, we work. 💪\n\n"
        "Explore the projects, get involved, and join the movement.\n\n"
        "📡 Available on Ethereum, Solana, and Base blockchains  \n"
        "✅ CertiK audit completed — verified & secured\n\n"
        "﹎﹎﹎﹎﹎﹎﹎\n"
        "🧭 Use the buttons below or type /menu to explore.\n"
        "﹎﹎﹎﹎﹎﹎﹎\n\n"
        "📢 Official Website: https://kendu.io  \n"
        "🧵 Twitter/X: https://x.com/KenduInu  \n"
        "📰 Reddit: https://www.reddit.com/r/KenduInu_Ecosystem  \n\n"
        "Made with ❤️ by the Kendu Community.",
        reply_markup=reply_markup
    )