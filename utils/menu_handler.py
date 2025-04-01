# utils/menu_handler.py

from telegram import Update, Message
from telegram.ext import ContextTypes

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE, msg_type="text") -> bool:
    """
    Checks if a menu-type message already exists and handles cleanup for slash/callback.
    Returns True if no new message should be sent.
    """

    message = update.message or (update.callback_query and update.callback_query.message)
    chat_id = message.chat_id if message else None

    # Clean up slash command message (e.g., /menu)
    if update.message:
        try:
            await update.message.delete()
        except Exception as e:
            print(f"⚠️ Failed to delete slash command message: {e}")

    # Clean up previous menu if type changed (e.g., image → text)
    old_msg_id = context.user_data.get("menu_msg_id")
    old_type = context.user_data.get("menu_msg_type", "text")

    # ✅ Avoid re-sending the same menu if it's already shown
    if old_msg_id and old_type == msg_type:
        return True  # Already showing, do nothing

    # ❌ Delete old message if media → text switch
    if old_msg_id and old_type != msg_type:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=old_msg_id)
        except Exception as e:
            print(f"⚠️ Failed to delete previous menu: {e}")

    return False  # Proceed to send new menu