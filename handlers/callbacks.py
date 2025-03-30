from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    await query.answer()  # Always acknowledge the query

    if data == "menu":
        keyboard = [
            [InlineKeyboardButton("🧠 About", callback_data="about")],
            [InlineKeyboardButton("🌐 Ecosystem", callback_data="ecosystem")],
            [InlineKeyboardButton("💰 Buy Kendu", callback_data="buy_kendu")],
            [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
            [InlineKeyboardButton("🧾 Contract Addresses", callback_data="contract_addresses")],
            [InlineKeyboardButton("🔗 Follow", callback_data="follow_links")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "📚 <b>Kendu Main Menu</b>\nTap an option below to explore:",
            parse_mode="HTML",
            reply_markup=reply_markup
        )
        return

    elif data == "about":
        await query.message.reply_text("🧠 Kendu is a decentralized ecosystem driven by community conviction.")
    elif data == "ecosystem":
        await query.message.reply_text("🌐 The Kendu ecosystem includes tools, community apps, and real-world products.")
    elif data == "buy_kendu":
        await query.message.reply_text("💰 You can buy Kendu on Ethereum, Solana, and Base. Visit /buykendu for steps.")
    elif data == "faq":
        await query.message.reply_text("❓ Visit /faq to read the most common questions.")
    elif data == "contract_addresses":
        await query.message.reply_text(
            "🧾 <b>Contract Addresses</b>\n"
            "ETH: 0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18\n"
            "SOL: 2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45\n"
            "BASE: 0xef73611F98DA6E57e0776317957af61B59E09Ed7",
            parse_mode="HTML"
        )
    elif data == "follow_links":
        await query.message.reply_text(
            "🔗 <b>Socials</b>\n"
            "🌐 Website: https://kendu.io\n"
            "💬 Telegram: https://t.me/Kendu\n"
            "📣 Twitter: https://x.com/KenduInu\n"
            "📰 Reddit: https://reddit.com/r/KenduInu_Ecosystem",
            parse_mode="HTML",
            disable_web_page_preview=True
        )
