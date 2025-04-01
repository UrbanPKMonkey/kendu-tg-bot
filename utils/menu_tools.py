from telegram.ext import ContextTypes


def reset_menu_context(context: ContextTypes.DEFAULT_TYPE):
    """
    Clears all tracked menu state from user_data.
    Useful for: /start, /logout, onboarding resets, full restarts.
    """
    context.user_data.pop("menu_msg_id", None)
    context.user_data.pop("menu_msg_type", None)
    context.user_data.pop("menu_msg_ids", None)
    print("🔁 Menu context reset")


def get_tracked_menu_state(context: ContextTypes.DEFAULT_TYPE):
    """
    Returns the currently tracked menu message IDs (list) and type.
    """
    return (
        context.user_data.get("menu_msg_ids", []),
        context.user_data.get("menu_msg_type", "text")
    )


def set_tracked_menu_state(context: ContextTypes.DEFAULT_TYPE, msg_id: int, msg_type: str = "text"):
    """
    Stores the latest menu message ID + type in user_data.
    Supports multiple tracked messages (media + text variants).
    """
    msg_ids = context.user_data.get("menu_msg_ids", [])
    msg_ids.append(msg_id)
    context.user_data["menu_msg_ids"] = msg_ids
    context.user_data["menu_msg_type"] = msg_type
    print(f"📌 Menu tracked → id={msg_id}, type={msg_type}")


async def safe_delete_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int, msg_id: int):
    """
    Attempts to delete a message silently. Use for cleaning old menu messages.
    """
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
    except Exception as e:
        print(f"⚠️ Failed to delete message ({msg_id}): {e}")
