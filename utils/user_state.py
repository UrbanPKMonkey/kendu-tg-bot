from telegram import Update
from telegram.ext import ContextTypes
from utils.menu_tools import get_tracked_menu_state, reset_menu_context, safe_delete_message

async def _reset_user_state(update: Update, context: ContextTypes.DEFAULT_TYPE, reset_start: bool = False):
    """
    Resets the user's menu/message state.

    - Deletes all tracked menu messages
    - Optionally deletes the /start message (if reset_start=True)
    - Clears tracked state in user_data
    """
    # Extract message and chat_id from the update (message or callback query)
    message = update.message or (update.callback_query and update.callback_query.message)
    chat_id = message.chat_id if message else None

    if not chat_id:
        print("⚠️ No chat_id found during reset")
        return

    # Retrieve the list of tracked messages
    old_msg_ids, _ = get_tracked_menu_state(context)
    start_msg_id = context.user_data.get("menu_start_msg_id")
    deleted = []

    # Iterate over the tracked messages and delete them
    for msg_id in old_msg_ids:
        if reset_start or msg_id != start_msg_id:
            await safe_delete_message(context, chat_id, msg_id)
            deleted.append(msg_id)

    # Reset all menu state and clear user_data related to menu
    reset_menu_context(context)

    if reset_start:
        context.user_data["menu_start_msg_id"] = None

    print(f"🧹 Reset user state. Deleted {len(deleted)} messages. Reset start: {reset_start}")
