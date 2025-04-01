# utils/menu_handler.py

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def menu_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    msg_type: str = "text",
    text: str = None,
    reply_markup: InlineKeyboardMarkup = None
):
    """
    Handles all smart logic for menu/message management:
    - Deletes slash command
    - Avoids duplicates
    - Deletes previous media/text if needed
    - Sends and tracks new message
    Returns: True if message already shown (no action), False if new one was sent.
    """

    message = update.message or (update.callback_query and update.callback_query.message)
    chat_id = message.chat_id if message else None

    # Delete slash command message
    if update.message:
        try:
            await update.message.delete()
        except Exception as e:
            print(f"⚠️ Failed to delete slash command message: {e}")

    old_msg_id = context.user_data.get("menu_msg_id")
    old_type = context.user_data.get("menu_msg_type", "text")

    # ✅ Already showing this message type — do nothing
    if old_msg_id and old_type == msg_type:
        return True

    # ❌ Different type (media ↔ text) — delete old
    if old_msg_id and old_type != msg_type:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=old_msg_id)
        except Exception as e:
            print(f"⚠️ Failed to delete previous menu: {e}")

    # 🧠 Send and track new menu text
    if msg_type == "text" and text:
        sent = await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
        context.user_data.update({
            "menu_msg_id": sent.message_id,
            "menu_msg_type": "text"
        })

    return False