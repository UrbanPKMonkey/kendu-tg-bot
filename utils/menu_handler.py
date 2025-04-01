# utils/menu_handler.py

from telegram.ext import ContextTypes

async def menu_handler(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    current_message,
    current_type: str = "text"
) -> bool:
    """
    Prevents duplicate menu messages and handles transitions (e.g., image → text).

    Args:
        context: Telegram context object with user_data.
        chat_id: ID of the chat where the menu is being shown.
        current_message: The incoming message or callback message.
        current_type: Type of the message we want to show ("text" or "photo").

    Returns:
        True if the current menu is already showing (skip sending).
        False if a new menu should be sent (continue flow).
    """
    old_msg_id = context.user_data.get("menu_msg_id")
    old_type = context.user_data.get("menu_msg_type", "text")
    current_msg_id = current_message.message_id if current_message else None

    # ✅ If same message ID and type — skip
    if old_msg_id and current_msg_id == old_msg_id and old_type == current_type:
        return True

    # 🔁 If type has changed — delete old message
    if old_msg_id and old_type != current_type:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=old_msg_id)
        except Exception as e:
            print(f"⚠️ Failed to delete old menu message: {e}")

    return False
