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

    if not chat_id:
        print("⚠️ No valid chat ID found — skipping menu handler")
        return True

    # 🧹 Delete /slash command message
    if update.message:
        try:
            await update.message.delete()
        except Exception as e:
            print(f"⚠️ Failed to delete slash command message: {e}")

    old_msg_ids = context.user_data.get("menu_msg_ids", [])
    old_type = context.user_data.get("menu_msg_type", "text")

    # ✅ Already showing same menu type — try to update reply markup
    if old_msg_ids and old_type == msg_type:
        try:
            await context.bot.edit_message_reply_markup(chat_id=chat_id, message_id=old_msg_ids[-1], reply_markup=reply_markup)
            return True
        except Exception:
            print("⚠️ Old menu not editable — replacing")

    # ❌ Delete ALL old menu messages
    for msg_id in old_msg_ids:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception:
            pass  # Message might already be gone

    # 🚀 Send new menu
    if msg_type == "text" and text:
        await send_tracked_menu_text(context, chat_id, text, reply_markup)
    elif msg_type == "photo" and text and photo:
        await send_tracked_menu_photo(context, chat_id, photo, text, reply_markup)
    elif msg_type == "video" and text and video:
        await send_tracked_menu_video(context, chat_id, video, text, reply_markup)
    elif msg_type == "document" and text and document:
        await send_tracked_menu_document(context, chat_id, document, text, reply_markup)

    return False
