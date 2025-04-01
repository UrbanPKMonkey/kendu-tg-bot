# handlers/sections/menu.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import ContextTypes

async def handle_menu(update: Update = None, context: ContextTypes.DEFAULT_TYPE = None, chat_id=None, message: Message = None):
    # Determine source
    query = update.callback_query if update else None
    message = query.message if query else message
    chat_id = message.chat_id if message else chat_id

    if query:
        await query.answer()

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

    # Try deleting previous menu message (if not a photo)
    try:
        if message and not message.photo:
            await message.delete()
    except Exception:
        pass

    sent = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    context.user_data["menu_msg_id"] = sent.message_id
    context.user_data["menu_msg_type"] = "text"

