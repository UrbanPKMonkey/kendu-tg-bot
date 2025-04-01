# utils/menu_handler.py

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.message_tools import (
    send_tracked_menu_text,
    send_tracked_menu_photo,
    send_tracked_menu_video,
    send_tracked_menu_document
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
    Returns True if no action needed (menu already shown), else False.
    """

    message = update.message or (update.callback_query and update.callback_query.message)
    chat_id = message.chat_id if message else None

    # 🧹 Delete /slash command message
    if update.message:
        try:
            await update.message.delete()
        except Exception as e:
            print(f"⚠️ Failed to delete slash command message: {e}")

    old_msg_id = context.user_data.get("menu_msg_id")
    old_type = context.user_data.get("menu_msg_type", "text")

    # ✅ Already showing the same type
    if old_msg_id and old_type == msg_type:
        return True

    # ❌ Switching types — delete old
    if old_msg_id and old_type != msg_type:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=old_msg_id)
        except Exception as e:
            print(f"⚠️ Failed to delete previous menu: {e}")

    # 🚀 Send new based on msg_type
    if msg_type == "text" and text:
        await send_tracked_menu_text(context, chat_id, text, reply_markup)
    elif msg_type == "photo" and text and photo:
        await send_tracked_menu_photo(context, chat_id, photo, text, reply_markup)
    elif msg_type == "video" and text and video:
        await send_tracked_menu_video(context, chat_id, video, text, reply_markup)
    elif msg_type == "document" and text and document:
        await send_tracked_menu_document(context, chat_id, document, text, reply_markup)

    return False
