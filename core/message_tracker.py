from telegram import Message, Update
from telegram.ext import ContextTypes


def track_bot_message(context: ContextTypes.DEFAULT_TYPE, message: Message):
    """Track any bot-sent message for future cleanup."""
    msg_ids = context.user_data.get("all_bot_msg_ids", [])
    msg_ids.append(message.message_id)
    context.user_data["all_bot_msg_ids"] = msg_ids
    print(f"📌 Tracked bot message: {message.message_id}")


def track_menu_message(context, message, msg_type: str, section_key: str = None):
    """Track menu message + register in full bot messages for restart cleanup."""
    context.user_data["menu_msg_ids"] = [message.message_id]
    context.user_data["menu_msg_type"] = msg_type
    if section_key:
        context.user_data["menu_section"] = section_key

    # ✅ Also track in all bot messages
    msg_ids = context.user_data.get("all_bot_msg_ids", [])
    msg_ids.append(message.message_id)
    context.user_data["all_bot_msg_ids"] = msg_ids

    print(f"📌 Tracked menu message: id={message.message_id}, type={msg_type}, section={section_key}")


def reset_tracked_messages(context: ContextTypes.DEFAULT_TYPE):
    """Clear all tracked message IDs from memory."""
    context.user_data["all_bot_msg_ids"] = []
    context.user_data["menu_msg_ids"] = []
    context.user_data["menu_msg_type"] = None
    context.user_data["menu_section"] = None
    print("🧼 Cleared all tracked message state")


async def delete_all_tracked(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete every message ever sent by the bot during this session."""
    chat_id = update.effective_chat.id
    all_ids = context.user_data.get("all_bot_msg_ids", [])
    for msg_id in all_ids:
        try:
            await context.bot.delete_message(chat_id, msg_id)
        except Exception:
            pass
    print(f"🧼 Deleted {len(all_ids)} tracked bot messages")
    reset_tracked_messages(context)


async def safe_delete_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int):
    """Safely delete a message and log result without crashing."""
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        print(f"🗑️ Deleted message {message_id}")
    except Exception as e:
        print(f"⚠️ Could not delete message {message_id}: {e}")
