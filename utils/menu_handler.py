from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.message_tools import (
    send_tracked_menu_text,
    send_tracked_menu_photo,
    send_tracked_menu_video,
    send_tracked_menu_document,
)
from utils.menu_tools import (
    get_tracked_menu_state,
    reset_menu_context,
    set_tracked_menu_state,
    safe_delete_message,
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
    Smart menu rendering + cleanup for text, photo, video, or document.
    Prevents clutter and ensures only one active menu is visible.
    Returns True if existing menu can be edited (no new one needed).
    """

    message = update.message or (update.callback_query and update.callback_query.message)
    chat_id = message.chat_id if message else None
    if not chat_id:
        print("⚠️ No chat_id found. Skipping menu handler.")
        return True

    # 🧹 Delete original slash command message
    if update.message:
        try:
            await update.message.delete()
        except Exception as e:
            print(f"⚠️ Failed to delete slash command: {e}")

    old_msg_ids, old_type = get_tracked_menu_state(context)

    # ✅ Try editing inline buttons if type is unchanged
    if old_msg_ids and old_type == msg_type:
        try:
            await context.bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=old_msg_ids[-1],
                reply_markup=reply_markup
            )
            print(f"♻️ Reused existing menu message (id={old_msg_ids[-1]})")
            return True
        except Exception:
            print("⚠️ Could not edit existing menu — deleting and sending new.")

    # ❌ Delete all old menu messages
    for msg_id in old_msg_ids:
        await safe_delete_message(context, chat_id, msg_id)

    # 🔄 Reset and track fresh menu state
    reset_menu_context(context)

    # 🚀 Send new menu by content type
    if msg_type == "text" and text:
        sent = await send_tracked_menu_text(context, chat_id, text, reply_markup)
    elif msg_type == "photo" and photo and text:
        sent = await send_tracked_menu_photo(context, chat_id, photo, text, reply_markup)
    elif msg_type == "video" and video and text:
        sent = await send_tracked_menu_video(context, chat_id, video, text, reply_markup)
    elif msg_type == "document" and document and text:
        sent = await send_tracked_menu_document(context, chat_id, document, text, reply_markup)
    else:
        print("⚠️ No valid menu content provided.")
        return True

    # ✅ Track newly sent message
    set_tracked_menu_state(context, sent.message_id, msg_type)
    return False
