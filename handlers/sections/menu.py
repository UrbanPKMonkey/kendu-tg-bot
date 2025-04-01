# handlers/sections/menu.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import ContextTypes

async def handle_menu(update: Update = None, context: ContextTypes.DEFAULT_TYPE = None, chat_id=None, message: Message = None):
    # Determine context
    query = update.callback_query if update else None
    is_slash = bool(update.message)
    message = query.message if query else message
    chat_id = message.chat_id if message else chat_id

    if query:
        await query.answer()

    # Delete slash command message
    if is_slash:
        try:
            await update.message.delete()
        except Exception:
            pass

    # Delete previous menu message if needed (image → text transition)
    old_msg_id = context.user_data.get("menu_msg_id")
    old_type = context.user_data.get("menu_msg_type", "text")

    if old_msg_id:
        try:
            if old_type == "photo":
                await context.bot.delete_message(chat_id=chat_id, message_id=old_msg_id)
        except Exception:
            pass

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


