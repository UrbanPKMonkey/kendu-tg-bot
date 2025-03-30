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
        caption="<b>Welcome to the Official Kendu Bot</b>\nTap below to begin exploring the Kendu ecosystem. 🚀",
        parse_mode="HTML",
        reply_markup=reply_markup
    )

    # 2️⃣ Follow-up message with full welcome info
    await update.message.reply_text(
        "<b>We don’t gamble, we work.</b> 💪\n\n"
        "Explore the projects, get involved, and join the movement.\n\n"
        "﹎﹎﹎﹎﹎﹎﹎\n\n"
        "🤖 Tap <code>/menu</code> to get started or explore:\n\n"
        "<code>/about</code>     → What is Kendu?\n"
        "<code>/eco</code>       → Our Ecosystem\n"
        "<code>/buykendu</code>  → How to Buy\n"
        "<code>/faq</code>       → Questions & Answers\n"
        "<code>/contracts</code> → Contract Addresses\n"
        "<code>/follow</code>    → Socials & Links\n"
        "﹎﹎﹎﹎﹎﹎﹎\n\n"
        "<b>🌐 Official Website:</b> <a href='https://kendu.io'>https://kendu.io</a>\n"
        "<b>💬 Telegram:</b> <a href='https://t.me/Kendu'>https://t.me/Kendu</a>\n"
        "<b>📣 Twitter/X:</b> <a href='https://x.com/KenduInu'>https://x.com/KenduInu</a>\n"
        "<b>📰 Reddit:</b> <a href='https://www.reddit.com/r/KenduInu_Ecosystem'>r/KenduInu_Ecosystem</a>\n\n"
        "⛓️ Available on Ethereum (ETH), Solana (SOL), and Base (BASE)\n"
        "<b>ETH:</b> 0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18\n"
        "<b>SOL:</b> 2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45\n"
        "<b>BASE:</b> 0xef73611F98DA6E57e0776317957af61B59E09Ed7\n\n"
        "✅ <i><a href='https://skynet.certik.com/projects/kendu-inu'>CertiK</a> audit completed</i>\n\n"
        "Made with ❤️ by the Kendu Community.",
        parse_mode="HTML",
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
        [InlineKeyboardButton("🔗 Follow", callback_data="follow_links")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🧭 <b>Explore the Kendu Ecosystem:</b>",
        reply_markup=reply_markup,
        parse_mode="HTML"
    ) 