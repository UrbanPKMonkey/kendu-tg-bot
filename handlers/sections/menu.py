# handlers/sections/menu.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import ContextTypes
from utils.menu_handler import menu_handler

async def handle_menu(update: Update = None, context: ContextTypes.DEFAULT_TYPE = None, chat_id=None, message: Message = None):
    # Determine context
    query = update.callback_query if update else None
    is_slash = bool(update.message)
    message = query.message if query else message
    chat_id = message.chat_id if message else chat_id

    if query:
        await query.answer()

    # Use shared menu_handler to avoid duplicates or re-sending
    if await menu_handler(context, chat_id, message, msg_type="text"):
        return

    # Send fresh text menu
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

    sent = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    context.user_data["menu_msg_id"] = sent.message_id
    context.user_data["menu_msg_type"] = "text"
