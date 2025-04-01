from telegram import Update
from telegram.ext import ContextTypes

from core.message_tracker import track_menu_message, get_tracked_menu_state, safe_delete_message


async def menu_renderer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    msg_type: str,
    text: str = None,
    photo: str = None,
    reply_markup=None,
    parse_mode: str = "HTML",
    section_key: str = None
):
    """
    Renders a menu message (text or photo), with smart edit or delete/resend logic.
    Tracks the message ID and section_key for re-use or cleanup later.
    """

    old_msg_ids, old_type, _ = get_tracked_menu_state(context)
    chat_id = update.effective_chat.id

    # If same type and message exists → try editing it
    if old_msg_ids and old_type == msg_type:
        try:
            if msg_type == "text" and text:
                sent = await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=old_msg_ids[-1],
                    text=text,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode
                )
                print(f"✏️ Edited text message: {sent.message_id}")
                track_menu_message(context, sent, msg_type, section_key)
                return sent

            elif msg_type == "photo" and text:
                sent = await context.bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=old_msg_ids[-1],
                    caption=text,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode
                )
                print(f"🖼️ Edited photo caption: {sent.message_id}")
                track_menu_message(context, sent, msg_type, section_key)
                return sent

        except Exception as e:
            print(f"⚠️ Old message not editable — switching to delete/send. Reason: {e}")
            await safe_delete_message(context, chat_id, old_msg_ids[-1])

    # Otherwise send a new message
    if msg_type == "text":
        sent = await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
        print(f"📌 Sent new text message: {sent.message_id}")

    elif msg_type == "photo":
        sent = await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
        print(f"📌 Sent new photo message: {sent.message_id}")

    else:
        raise ValueError(f"Unsupported msg_type: {msg_type}")

    track_menu_message(context, sent, msg_type, section_key)
    return sent
