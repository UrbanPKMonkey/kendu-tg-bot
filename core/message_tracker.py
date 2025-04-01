from telegram import Message, Update
from telegram.ext import ContextTypes
from functools import wraps

# === 🧠 Track a message the bot sends ===
def track_bot_message(context: ContextTypes.DEFAULT_TYPE, message: Message):
    """Track any bot-sent message for future cleanup."""
    msg_ids = context.user_data.get("all_bot_msg_ids", [])
    msg_ids.append(message.message_id)
    context.user_data["all_bot_msg_ids"] = msg_ids
    print(f"📌 Tracked bot message: {message.message_id}")


# === 🧠 Track a menu message (also tracked as bot message) ===
def track_menu_message(context, message, msg_type: str, section_key: str = None):
    """Track menu message + register in full bot messages for restart cleanup."""
    context.user_data["menu_msg_ids"] = [message.message_id]
    context.user_data["menu_msg_type"] = msg_type
    if section_key:
        context.user_data["menu_section"] = section_key

    # Also add to all_bot_msg_ids for full deletion
    msg_ids = context.user_data.get("all_bot_msg_ids", [])
    msg_ids.append(message.message_id)
    context.user_data["all_bot_msg_ids"] = msg_ids

    print(f"📌 Tracked menu message: id={message.message_id}, type={msg_type}, section={section_key}")


# === 🧼 Reset all tracked message state ===
def reset_tracked_messages(context: ContextTypes.DEFAULT_TYPE):
    """Clear all bot and menu message IDs from memory."""
    context.user_data["all_bot_msg_ids"] = []
    context.user_data["menu_msg_ids"] = []
    context.user_data["menu_msg_type"] = None
    context.user_data["menu_section"] = None
    print("🧼 Cleared all tracked message state")


# === 🧹 Delete everything the bot ever sent this session ===
async def delete_all_tracked(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete every message ever sent by the bot during this session."""
    chat_id = update.effective_chat.id
    all_ids = context.user_data.get("all_bot_msg_ids", []) or []
    deleted = 0

    for msg_id in all_ids:
        try:
            await context.bot.delete_message(chat_id, msg_id)
            deleted += 1
        except Exception:
            pass

    print(f"🧼 Deleted {deleted} tracked bot messages")
    reset_tracked_messages(context)


# === 🪄 Unified Slash Command Wrapper ===
def wrap_command_handler(handler_func):
    """
    Wraps a slash command handler:
    - Deletes the user's slash command message
    - Proceeds to the original handler
    """
    @wraps(handler_func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        try:
            if update.message:
                await update.message.delete()
                print(f"🧼 Deleted slash command: {update.message.text}")
        except Exception as e:
            print(f"⚠️ Failed to delete slash command: {e}")
        return await handler_func(update, context, *args, **kwargs)
    return wrapper
