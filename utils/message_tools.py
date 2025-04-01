from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update,
    Message
)
from telegram.ext import ContextTypes
from io import BytesIO
import requests
from PIL import Image


# === Unified Send/Track Helper ===
def _track_menu_message(context, sent: Message, msg_type: str):
    context.user_data["menu_msg_ids"] = [sent.message_id]
    context.user_data["menu_msg_type"] = msg_type
    return sent  # explicitly returns Message object


# === Clean Smart Senders ===

async def send_tracked_menu_text(context, chat_id, text, reply_markup):
    sent = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    return _track_menu_message(context, sent, "text")


async def send_tracked_menu_photo(context, chat_id, photo, caption, reply_markup):
    sent = await context.bot.send_photo(
        chat_id=chat_id,
        photo=photo,
        caption=caption,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    return _track_menu_message(context, sent, "photo")


async def send_tracked_menu_video(context, chat_id, video, caption, reply_markup):
    sent = await context.bot.send_video(
        chat_id=chat_id,
        video=video,
        caption=caption,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    return _track_menu_message(context, sent, "video")


async def send_tracked_menu_document(context, chat_id, document, caption, reply_markup):
    sent = await context.bot.send_document(
        chat_id=chat_id,
        document=document,
        caption=caption,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    return _track_menu_message(context, sent, "document")


# === Smart Editor / Replacer ===

async def smart_send_or_edit(
    query=None,
    context: ContextTypes.DEFAULT_TYPE = None,
    new_text: str = "",
    reply_markup: InlineKeyboardMarkup = None,
    parse_mode: str = "HTML",
    message_override: Message = None
):
    message = query.message if query else message_override
    chat_id = message.chat_id if message else None
    old_msg_id = context.user_data.get("menu_msg_id")
    old_type = context.user_data.get("menu_msg_type", "text")
    force_new = bool(message_override) or old_type != "text"

    if old_msg_id and not force_new:
        try:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=old_msg_id,
                text=new_text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
            return
        except Exception:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=old_msg_id)
            except Exception:
                pass

    if message_override:
        try:
            await message_override.delete()
        except Exception:
            pass

    sent = await context.bot.send_message(
        chat_id=chat_id,
        text=new_text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )
    _track_menu_message(context, sent, "text")
    return sent  # return explicitly for clarity


async def delete_and_send_new(update, context, text, reply_markup=None, parse_mode="HTML"):
    try:
        if update.message:
            await update.message.delete()
        elif update.callback_query:
            await update.callback_query.message.delete()
    except Exception as e:
        print(f"⚠️ Failed to delete message: {e}")

    sent = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )
    return sent  # explicitly return Message object


# === Visual Tools ===

async def add_black_background_to_image(image_url: str) -> BytesIO:
    response = requests.get(image_url)
    original = Image.open(BytesIO(response.content)).convert("RGBA")

    background = Image.new("RGB", original.size, (0, 0, 0))
    background.paste(original, mask=original.split()[3])

    output = BytesIO()
    output.name = "with_black_bg.png"
    background.save(output, format="PNG")
    output.seek(0)
    return output


# === Static Menus ===

def get_contracts_text_and_markup():
    text = (
        "🧾 <b>Contract Addresses</b>\n\n"
        "⚫ <b>Ethereum (ETH):</b>\n"
        "<code>   0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18</code>\n\n"
        "🟣 <b>Solana (SOL):</b>\n"
        "<code>   2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45</code>\n\n"
        "🔵 <b>Base (BASE):</b>\n"
        "<code>   0xef73611F98DA6E57e0776317957af61B59E09Ed7</code>"
    )

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="menu")]
    ])

    return text, reply_markup


async def edit_menu_response(context, chat_id, message_id, text, reply_markup):
    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )


# === Clear Menus ===

async def clear_all_menus(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    """
    Deletes all tracked menu messages across any type (text, photo, etc.).
    Useful for logout, restart, or global cleanup.
    """
    old_msg_ids = context.user_data.get("menu_msg_ids", [])

    for msg_id in old_msg_ids:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception:
            pass

    # Reset user_data menu tracking
    context.user_data["menu_msg_ids"] = []
    context.user_data["menu_msg_type"] = None
