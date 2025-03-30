from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        "**Welcome to the Official Kendu Bot** — your all-in-one portal to the decentralized Kendu ecosystem.\n\n"
        "**We don’t gamble, we work.** 💪\n\n"
        "Explore the projects, get involved, and join the movement.\n\n"
        "✅ CertiK audit completed — verified & secured\n\n"
        "﹎﹎﹎﹎﹎﹎﹎\n\n"
        "🧭 Tap /menu to get started or explore:\n\n"
        "/about        → What is Kendu?  \n"
        "/eco          → Our Ecosystem  \n"
        "/buykendu     → How to Buy  \n"
        "/faq          → Questions & Answers  \n"
        "/contracts    → Contract Addresses  \n"
        "/follow       → Socials & Links  \n"
        "﹎﹎﹎﹎﹎﹎﹎\n\n"
        "📢 **Official Website:** https://kendu.io  \n"
        "📢 **Telegram:** https://t.me/Kendu  \n"        
        "🧵 **Twitter/X:** https://x.com/KenduInu  \n"
        "📰 **Reddit:** https://www.reddit.com/r/KenduInu_Ecosystem  \n\n"
        "📡 Available on Ethereum, Solana, and Base blockchains  \n\n"        
        "**Contract Addresses:**  \n"
        "**ETH:**  0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18\n"
        "**SOL:**  2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45\n"
        "**BASE:** 0xef73611F98DA6E57e0776317957af61B59E09Ed7\n\n"                        
        "Made with ❤️ by the Kendu Community.",
        parse_mode="Markdown",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Reuse the same layout from /start
    keyboard = [
        [InlineKeyboardButton("🧠 About", callback_data="about")],
        [InlineKeyboardButton("🌐 Ecosystem", callback_data="ecosystem")],
        [InlineKeyboardButton("💰 Buy Kendu", callback_data="buy_kendu")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("🧾 Contract Addresses", callback_data="contract_addresses")],
        [InlineKeyboardButton("🔗 Follow", callback_data="follow_links")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🧭 *Explore the Kendu Ecosystem:*",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )    