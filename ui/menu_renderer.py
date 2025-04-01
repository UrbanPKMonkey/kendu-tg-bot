from telegram import Update, InlineKeyboardMarkup, Message
from telegram.ext import ContextTypes

from core.menu_state import get_tracked_menu_state, safe_delete_message
from core.message_tracker import track_menu_message


async def menu_renderer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    msg_type: str = "text",
    text: str = None,
    reply_markup: InlineKeyboardMarkup = None,
    photo=None,
    video=None,
    document=None
) -> Message:
    """
    Handles rendering of any menu (text, photo, video, document) with proper message tracking.
    Deletes old messages if switching media type or fails to edit.
    """
    message = update.message or (update.callback_query and update.callback_query.message)
    chat_id = message.chat_id if message else None
    if not chat_id:
        print("⚠️ No chat_id found.")
        return None

    last_start_msg_id = context.user_data.get("menu_start_msg_id")
    if update.message and (last_start_msg_id != update.message.message_id):
        try:
            await update.message.delete()
        except Exception as e:
            print(f"⚠️ Failed to delete slash command: {e}")

    old_msg_ids, old_type = get_tracked_menu_state(context)
    can_edit_same_type = old_msg_ids and old_type == msg_type

    if can_edit_same_type:
        try:
            await context.bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=old_msg_ids[-1],
                reply_markup=reply_markup
            )
            return await context.bot.get_message(chat_id=chat_id, message_id=old_msg_ids[-1])
        except Exception:
            print("⚠️ Old message not editable — switching to delete/send.")

    for msg_id in old_msg_ids:
        if msg_id != last_start_msg_id:
            await safe_delete_message(context, chat_id, msg_id)

    # === 🖼 Send New Message ===
    if msg_type == "text" and text:
        sent = await context.bot.send_message(
            chat_id,
            text,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    elif msg_type == "photo" and photo and text:
        sent = await context.bot.send_photo(
            chat_id,
            photo,
            caption=text,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    elif msg_type == "video" and video and text:
        sent = await context.bot.send_video(
            chat_id,
            video,
            caption=text,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    elif msg_type == "document" and document and text:
        sent = await context.bot.send_document(
            chat_id,
            document,
            caption=text,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    else:
        print("⚠️ Invalid or missing content for menu_renderer")
        return None

    # ✅ Track the new message
    track_menu_message(context, sent, msg_type)
    return sent
