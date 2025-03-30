from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    await query.answer()  # Acknowledge the button tap

    # 🔙 Back to main menu button layout
    back_button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
    )

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

        await query.message.edit_text(
            "🤖 <b>Kendu Main Menu</b>\n\nTap an option below to explore:",
            parse_mode="HTML",
            reply_markup=reply_markup
        )

    elif data == "about":
        await query.message.edit_text(
            "🧠 <b>About Kendu</b>\n\n"
            "Kendu is a decentralized ecosystem driven by community conviction.",
            parse_mode="HTML",
            reply_markup=back_button
        )

    elif data == "ecosystem":
        await query.message.edit_text(
            "🌐 <b>Kendu Ecosystem</b>\n\n"
            "The Kendu ecosystem includes tools, community apps, and real-world products.",
            parse_mode="HTML",
            reply_markup=back_button
        )

    elif data == "buy_kendu":
        await query.message.edit_text(
            "💰 <b>How to Buy Kendu</b>\n\n"
            "Kendu is available on Ethereum, Solana, and Base.\n\n"
            "Visit /buykendu to learn more.",
            parse_mode="HTML",
            reply_markup=back_button
        )

    elif data == "faq":
        await query.message.edit_text(
            "❓ <b>FAQ</b>\n\n"
            "Answers to common questions are available at /faq",
            parse_mode="HTML",
            reply_markup=back_button
        )

    elif data == "contract_addresses":
        await query.message.edit_text(
            "🧾 <b>Contract Addresses</b>\n\n"
            "ETH: 0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18\n"
            "SOL: 2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45\n"
            "BASE: 0xef73611F98DA6E57e0776317957af61B59E09Ed7",
            parse_mode="HTML",
            reply_markup=back_button
        )

    elif data == "follow_links":
        await query.message.edit_text(
            "🔗 <b>Social Links</b>\n\n"
            "🌐 <a href='https://kendu.io'>kendu.io</a>\n"
            "💬 <a href='https://t.me/Kendu'>Telegram</a>\n"
            "📣 <a href='https://x.com/KenduInu'>Twitter/X</a>\n"
            "📰 <a href='https://www.reddit.com/r/KenduInu_Ecosystem'>Reddit</a>",
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=back_button
        )
