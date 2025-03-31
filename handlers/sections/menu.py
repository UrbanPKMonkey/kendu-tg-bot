# handlers/sections/menu.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def handle_menu(update: Update = None, context: ContextTypes.DEFAULT_TYPE = None, message_override=None):
    """Handles the main menu rendering and cleanup."""
    query = update.callback_query if update else None
    chat_id = (query.message.chat_id if query else message_override.chat_id)

    # ✅ Delete old message if it's NOT a photo (i.e. not from /start)
    try:
        current_message = query.message if query else message_override
        if current_message and not current_message.photo:
            await current_message.delete()
    except Exception:
        pass  # Ignore deletion errors

    # 📲 Build menu text and buttons
    text = (
        "🤖 <b>Kendu Main Menu</b>\n\n"
        "Tap an option below to explore:"
    )

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🧠 About", callback_data="about")],
        [InlineKeyboardButton("🌐 Ecosystem", callback_data="ecosystem")],
        [InlineKeyboardButton("💰 Buy Kendu", callback_data="buy_kendu")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("🧾 Contract Addresses", callback_data="contract_addresses")],
        [InlineKeyboardButton("🔗 Follow", callback_data="follow_links")]
    ])

    # ✅ Send new menu message
    sent = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    # 💾 Track for back-navigation and cleanup
    context.user_data["menu_msg_id"] = sent.message_id
    context.user_data["menu_msg_type"] = "text"
