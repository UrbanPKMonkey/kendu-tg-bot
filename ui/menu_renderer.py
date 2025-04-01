from telegram import Update
from telegram.ext import ContextTypes

from core.message_tracker import track_menu_message  # ✅ Only this from message_tracker
from core.menu_state import get_tracked_menu_state, safe_delete_message  # ✅ Correct source

async def menu_renderer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    msg_type: str,
    text: str = None,
    photo: str = None,
    video: str = None,
    document: str = None,
    animation: str = None,
    reply_markup=None,
    parse_mode: str = "HTML",
    section_key: str = None
):
    """
    🔁 Renders a menu message with smart edit or delete/send fallback.
    Supports "text", "photo", "video", "document", and "animation".
    Tracks section identity for clean re-renders.
    """
    old_msg_ids, old_type, old_section = get_tracked_menu_state(context)
    chat_id = update.effective_chat.id

    # 🔄 If message type has changed → delete old one (unless it's from /start)
    if old_msg_ids and old_type != msg_type:
        if old_section != "start":
            print(f"🔄 Message type changed ({old_type} → {msg_type}) — deleting old message.")
            await safe_delete_message(context, chat_id, old_msg_ids[-1])
            old_msg_ids = []
        else:
            print("⏭️ Preserving welcome screen message — skipping deletion.")

    # ✏️ Try editing old message of the same type
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
            elif msg_type == "photo" and text:
                sent = await context.bot.edit_message_caption(
                    chat_id=chat_id,
                    message_id=old_msg_ids[-1],
                    caption=text,
                    reply_markup=reply_markup,
                    parse_mode=parse_mode
                )
            elif msg_type in ["video", "document", "animation"]:
                raise Exception("Edit not supported for this type")
            else:
                raise Exception("Unknown msg_type")

            print(f"✏️ Edited {msg_type} message: {sent.message_id}")
            track_menu_message(context, sent, msg_type, section_key)
            return sent

        except Exception as e:
            print(f"⚠️ Cannot edit {msg_type} — deleting and resending. Reason: {e}")
            await safe_delete_message(context, chat_id, old_msg_ids[-1])
            old_msg_ids = []

    # ➕ Send a new message
    if msg_type == "text":
        sent = await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )

    elif msg_type == "photo":
        sent = await context.bot.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )

    elif msg_type == "video":
        sent = await context.bot.send_video(
            chat_id=chat_id,
            video=video,
            caption=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )

    elif msg_type == "document":
        sent = await context.bot.send_document(
            chat_id=chat_id,
            document=document,
            caption=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )

    elif msg_type == "animation":
        sent = await context.bot.send_animation(
            chat_id=chat_id,
            animation=animation,
            caption=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )

    else:
        raise ValueError(f"❌ Unsupported msg_type: {msg_type}")

    print(f"📌 Sent new {msg_type} message: {sent.message_id}")
    track_menu_message(context, sent, msg_type, section_key)
    return sent
