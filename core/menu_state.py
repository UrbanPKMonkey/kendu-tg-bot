from telegram.ext import ContextTypes

def reset_menu_context(context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("menu_msg_id", None)
    context.user_data.pop("menu_msg_type", None)
    context.user_data.pop("menu_msg_ids", None)
    print("🔁 Menu context reset")

def get_tracked_menu_state(context):
    return (
        context.user_data.get("menu_msg_ids"),
        context.user_data.get("menu_msg_type"),
        context.user_data.get("menu_section")
    )

def set_tracked_menu_state(context: ContextTypes.DEFAULT_TYPE, msg_id: int, msg_type: str = "text"):
    msg_ids = context.user_data.get("menu_msg_ids", [])
    if msg_id not in msg_ids:
        msg_ids.append(msg_id)
        context.user_data["menu_msg_ids"] = msg_ids
        context.user_data["menu_msg_type"] = msg_type
        print(f"📌 Menu tracked → id={msg_id}, type={msg_type}")

async def safe_delete_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int, msg_id: int):
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        print(f"🗑️ Deleted message {msg_id}")
    except Exception as e:
        print(f"⚠️ Failed to delete message {msg_id}: {e}")

async def delete_all_bot_messages(update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    all_msg_ids = context.user_data.get("all_bot_msg_ids", [])
    for msg_id in all_msg_ids:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception:
            pass
    print(f"🧼 Deleted {len(all_msg_ids)} total bot messages")
    context.user_data["all_bot_msg_ids"] = []
    context.user_data["menu_msg_ids"] = []
    context.user_data["menu_msg_type"] = None

async def should_skip_section_render(update, context, section_type: str = "text", section_key: str = None) -> bool:
    try:
        if update.message:
            await update.message.delete()
    except Exception as e:
        print(f"⚠️ Failed to delete slash command: {e}")

    # 🟢 Force refresh logic from 'Refresh Price' button
    if context.user_data.get("force_refresh"):
        print("🔁 Refresh forced — not skipping render.")
        context.user_data.pop("force_refresh", None)
        return False

    old_msg_ids, old_type, old_section = get_tracked_menu_state(context)

    if (
        old_type == section_type
        and old_msg_ids
        and section_key
        and old_section == section_key
    ):
        print(f"⏭️ {section_key.upper()} already active — skipping re-render")
        return True

    return False
