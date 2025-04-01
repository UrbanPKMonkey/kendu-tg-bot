# utils/user_state.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.menu_tools import get_tracked_menu_state, reset_menu_context, safe_delete_message

async def _reset_user_state(update: Update, context: ContextTypes.DEFAULT_TYPE, reset_start: bool = False):
    """
    Resets the user's menu/message state.
    
    - Deletes tracked menu messages
    - Optionally deletes the /start message
    - Clears user_data keys related to menu navigation
    """
    message = update.message or (update.callback_query and update.callback_query.message)
    chat_id = message.chat_id if message else None

    if not chat_id:
        print("⚠️ No chat_id found during reset")
        return

    old_msg_ids, _ = get_tracked_menu_state(context)
    start_msg_id = context.user_data.get("menu_start_msg_id")

    for msg_id in old_msg_ids:
        if reset_start or msg_id != start_msg_id:
            await safe_delete_message(context, chat_id, msg_id)

    reset_menu_context(context)
