from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🤖 Menu", callback_data="menu")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    
    # 1️⃣ Show image with short caption + button
    await update.message.reply_photo(
        photo="https://i.imgur.com/r0i7fuG.png",
        caption=(
            "<b>Welcome to the Official Kendu Bot</b> — your all-in-one portal to the decentralized Kendu ecosystem.\n\n"
            "<b>We don’t gamble, we work.</b> 💪\n\n"
            "Explore the projects, get involved, and join the movement.\n\n"
            "﹎﹎﹎﹎﹎﹎﹎\n\n"
            "🤖 Tap /menu to get started or explore:\n\n"
            "/about     → What is Kendu?\n"
            "/eco       → Our Ecosystem\n"
            "/buykendu  → How to Buy\n"
            "/faq       → Questions & Answers\n"
            "/contracts → Contract Addresses\n"
            "/follow    → Socials & Links\n"
            "﹎﹎﹎﹎﹎﹎﹎\n\n"
            "<b>🌐 Official Website:</b> <a href='https://kendu.io'>https://kendu.io</a>\n"
            "<b>💬 Telegram:</b> <a href='https://t.me/Kendu'>https://t.me/Kendu</a>\n"
            "<b>📣 Twitter/X:</b> <a href='https://x.com/KenduInu'>https://x.com/KenduInu</a>\n"
            "<b>📰 Reddit:</b> <a href='https://www.reddit.com/r/KenduInu_Ecosystem'>r/KenduInu_Ecosystem</a>\n\n"
            "⛓️ Available on <b>Ethereum (ETH)</b>, <b>Solana (SOL)</b>, and <b>Base (BASE)</b>\n"
            "⚫ <b>Ethereum (ETH):</b>\n"
            "<code>   0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18</code>\n\n"
            "🟣 <b>Solana (SOL):</b>\n"
            "<code>   2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45</code>\n\n"
            "🔵 <b>Base (BASE):</b>\n"
            "<code>   0xef73611F98DA6E57e0776317957af61B59E09Ed7</code>\n\n"
            "✅ <i><a href='https://skynet.certik.com/projects/kendu-inu'>CertiK</a> audit completed</i>\n\n"
            "Made with ❤️ by the Kendu Community."
            ),
        parse_mode="HTML",
        reply_markup=reply_markup
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧠 About", callback_data="about")],
        [InlineKeyboardButton("🌐 Ecosystem", callback_data="ecosystem")],
        [InlineKeyboardButton("💰 Buy Kendu", callback_data="buy_kendu")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("🧾 Contract Addresses", callback_data="contract_addresses")],
        [InlineKeyboardButton("🔗 Follow", callback_data="follow_links")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Detect how the command was triggered
    if update.callback_query:
        await update.callback_query.message.reply_text(
            "🤖 <b>Kendu Main Menu</b>\n\nTap an option below to explore:",
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "🤖 <b>Kendu Main Menu</b>\n\nTap an option below to explore:",
            parse_mode="HTML",
            reply_markup=reply_markup
        )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧠 Tap the Menu and choose 'About' to learn what Kendu is all about!")

async def eco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌐 Use the Menu and tap 'Ecosystem' to dive into all Kendu is building!")

async def buykendu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 Hit 'Buy Kendu' in the Menu to learn how to get $KENDU on ETH, SOL & BASE.")

async def contracts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🧾 Hit 'Contract Addresses' in the Menu to get full chain listings.")

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❓ Check out the FAQ in the Menu to find answers to common questions.")

async def follow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔗 Head to 'Follow' in the Menu to discover Kendu's official links.")        