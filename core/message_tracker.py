from telegram import Message, Update
from telegram.ext import ContextTypes

def track_bot_message(context: ContextTypes.DEFAULT_TYPE, message: Message):
    """Track any bot-sent message for future cleanup."""
    msg_ids = context.user_data.get("all_bot_msg_ids", [])
    msg_ids.append(message.message_id)
    context.user_data["all_bot_msg_ids"] = msg_ids
    print(f"📌 Tracked bot message: {message.message_id}")

def track_menu_message(context: ContextTypes.DEFAULT_TYPE, message: Message, msg_type: str):
    """Track menu-specific message ID and type."""
    context.user_data["menu_msg_ids"] = [message.message_id]
    context.user_data["menu_msg_type"] = msg_type
    track_bot_message(context, message)
    print(f"📌 Tracked menu message: id={message.message_id}, type={msg_type}")

def reset_tracked_messages(context: ContextTypes.DEFAULT_TYPE):
    """Clear all bot and menu message IDs from memory."""
    context.user_data["all_bot_msg_ids"] = []
    context.user_data["menu_msg_ids"] = []
    context.user_data["menu_msg_type"] = None
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
