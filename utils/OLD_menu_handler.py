from telegram import Update, InlineKeyboardMarkup, Message
from telegram.ext import ContextTypes
from core.message_tracker import (
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
) -> Message:
    """
    Smart menu rendering + cleanup for text, photo, video, and document.
    Tracks message IDs to prevent clutter and ensure clean transitions.
    Always returns the resulting Message object.
    """

    # Get the chat ID from either message or callback query
    message = update.message or (update.callback_query and update.callback_query.message)
    chat_id = message.chat_id if message else None

    if not chat_id:
        print("⚠️ No chat_id found. Skipping menu handling.")
        return None

    # Get the last /start message ID (to preserve it)
    last_start_msg_id = context.user_data.get("menu_start_msg_id")

    # Clean up the command message if it's not the preserved /start message
    if update.message and (last_start_msg_id != update.message.message_id):
        try:
            await update.message.delete()
        except Exception as e:
            print(f"⚠️ Failed to delete slash command: {e}")

    # Get previously tracked messages
    old_msg_ids = context.user_data.get("menu_msg_ids", [])
    old_type = context.user_data.get("menu_msg_type", None)

    # Try editing the last message if it's the same type (e.g., text, photo, etc.)
    if old_msg_ids and old_type == msg_type:
        try:
            await context.bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=old_msg_ids[-1],
                reply_markup=reply_markup
            )
            # Return the reused message
            return await context.bot.get_message(chat_id=chat_id, message_id=old_msg_ids[-1])
        except Exception:
            print("⚠️ Old message not editable, sending new.")

    # Delete all old tracked messages (except for the /start message)
    for msg_id in old_msg_ids:
        if msg_id != last_start_msg_id:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            except Exception as e:
                print(f"⚠️ Failed to delete old message {msg_id}: {e}")

    # Send a new menu message based on type
    if msg_type == "text" and text:
        return await send_tracked_menu_text(context, chat_id, text, reply_markup)
    elif msg_type == "photo" and photo and text:
        return await send_tracked_menu_photo(context, chat_id, photo, text, reply_markup)
    elif msg_type == "video" and video and text:
        return await send_tracked_menu_video(context, chat_id, video, text, reply_markup)
    elif msg_type == "document" and document and text:
        return await send_tracked_menu_document(context, chat_id, document, text, reply_markup)

    print("⚠️ Invalid or missing content for menu_handler")
    return None
