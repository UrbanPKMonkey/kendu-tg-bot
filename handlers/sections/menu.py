# handlers/sections/menu.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import ContextTypes
from utils.menu_handler import menu_handler

async def handle_menu(update: Update = None, context: ContextTypes.DEFAULT_TYPE = None, chat_id=None, message: Message = None):
    # Determine source
    query = update.callback_query if update else None
    message = query.message if query else message
    chat_id = message.chat_id if message else chat_id

    if query:
        await query.answer()

    # If triggered by slash command, delete that command message
    if update and update.message:
        try:
            await update.message.delete()
        except Exception:
            pass

    # Build menu
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

    # Use universal menu handler to avoid duplication or ghost messages
    await menu_handler(context, chat_id, text, reply_markup, message)
