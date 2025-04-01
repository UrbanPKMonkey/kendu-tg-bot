from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.message_tools import (
    send_tracked_menu_text,
    send_tracked_menu_photo,
    send_tracked_menu_video,
    send_tracked_menu_document,
)

async def menu_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    msg_type: str = "text",
    text: str = None,
    reply_markup: InlineKeyboardMarkup = None,
    photo=None,
    video=None,
    document=None
):
    """
    Smart menu rendering + cleanup for text, photo, video, and document.
    Tracks message IDs to prevent clutter and ensure clean transitions.
    Returns True if no new message is needed (duplicate), else False.
    """
    
    message = update.message or (update.callback_query and update.callback_query.message)
    chat_id = message.chat_id if message else None

    if not chat_id:
        print("⚠️ No chat_id found. Skipping menu handling.")
        return True

    # Skip deletion if it's the start message (stored in context)
    last_start_msg_id = context.user_data.get("menu_start_msg_id")

    # Delete original slash command message unless it's the start message
    if update.message and (last_start_msg_id != update.message.message_id):
        try:
            await update.message.delete()
        except Exception as e:
            print(f"⚠️ Failed to delete slash command: {e}")

    old_msg_ids = context.user_data.get("menu_msg_ids", [])
    old_type = context.user_data.get("menu_msg_type", None)

    # ✅ Attempt edit if same type
    if old_msg_ids and old_type == msg_type:
        try:
            await context.bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=old_msg_ids[-1],
                reply_markup=reply_markup
            )
            return True
        except Exception:
            print("⚠️ Old message not editable, sending new.")

    # ❌ Delete all old tracked messages unless the last one was /start
    for msg_id in old_msg_ids:
        if msg_id != last_start_msg_id:  # Don't delete the /start message
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except Exception:
                pass  # Already deleted

    # 🚀 Send new menu by type
    if msg_type == "text" and text:
        await send_tracked_menu_text(context, chat_id, text, reply_markup)
    elif msg_type == "photo" and photo and text:
        await send_tracked_menu_photo(context, chat_id, photo, text, reply_markup)
    elif msg_type == "video" and video and text:
        await send_tracked_menu_video(context, chat_id, video, text, reply_markup)
    elif msg_type == "document" and document and text:
        await send_tracked_menu_document(context, chat_id, document, text, reply_markup)

    return False
