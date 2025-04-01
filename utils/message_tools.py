from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update,
    InputMediaPhoto,
    Message,
)
from telegram.ext import ContextTypes
from io import BytesIO
import requests
from PIL import Image


async def smart_send_or_edit(
    query=None,
    context: ContextTypes.DEFAULT_TYPE = None,
    new_text: str = "",
    reply_markup: InlineKeyboardMarkup = None,
    parse_mode: str = "HTML",
    message_override: Message = None
):
    """
    Edits or sends a new message depending on interaction context.
    Automatically deletes old message if necessary.
    """
    if query:
        chat_id = query.message.chat_id
        message = query.message
    elif message_override:
        chat_id = message_override.chat_id
        message = message_override
    else:
        raise ValueError("No valid message or query provided to smart_send_or_edit.")

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
    context.user_data["menu_msg_id"] = sent.message_id
    context.user_data["menu_msg_type"] = "text"


async def delete_and_send_new(update, context, text, reply_markup=None, parse_mode="HTML"):
    """Deletes the previous message (if applicable) and sends a fresh new message."""
    try:
        if update.message:
            await update.message.delete()
        elif update.callback_query:
            await update.callback_query.message.delete()
    except Exception as e:
        print(f"⚠️ Failed to delete message: {e}")

    new_msg = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )
    return new_msg


async def add_black_background_to_image(image_url: str) -> BytesIO:
    """
    Adds a black background behind transparent PNGs for Telegram compatibility.
    """
    response = requests.get(image_url)
    original = Image.open(BytesIO(response.content)).convert("RGBA")

    background = Image.new("RGB", original.size, (0, 0, 0))
    background.paste(original, mask=original.split()[3])

    output = BytesIO()
    output.name = "with_black_bg.png"
    background.save(output, format="PNG")
    output.seek(0)
    return output


def get_contracts_text_and_markup():
    """
    Returns contract text + back button markup.
    """
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
    """Edits an existing tracked menu message by ID."""
    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )


# ✅ New: Shared tracked text message sender
async def send_tracked_menu_text(context, chat_id, text, reply_markup):
    """
    Sends a new text message and tracks it in user_data for back/duplicate logic.
    """
    sent = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    context.user_data.update({
        "menu_msg_id": sent.message_id,
        "menu_msg_type": "text"
    })


# ✅ New: Shared tracked photo sender
async def send_tracked_menu_photo(context, chat_id, photo, caption, reply_markup):
    """
    Sends a new photo message and tracks it in user_data for back/duplicate logic.
    """
    sent = await context.bot.send_photo(
        chat_id=chat_id,
        photo=photo,
        caption=caption,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    context.user_data.update({
        "menu_msg_id": sent.message_id,
        "menu_msg_type": "photo"
    })


# ✅ New: Shared tracked video sender
async def send_tracked_menu_video(context, chat_id, video, caption, reply_markup):
    """
    Sends a new video message and tracks it in user_data for back/duplicate logic.
    """
    sent = await context.bot.send_video(
        chat_id=chat_id,
        video=video,
        caption=caption,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    context.user_data.update({
        "menu_msg_id": sent.message_id,
        "menu_msg_type": "video"
    })


# ✅ New: Shared tracked document sender
async def send_tracked_menu_document(context, chat_id, document, caption, reply_markup):
    """
    Sends a new document and tracks it in user_data for back/duplicate logic.
    """
    sent = await context.bot.send_document(
        chat_id=chat_id,
        document=document,
        caption=caption,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    context.user_data.update({
        "menu_msg_id": sent.message_id,
        "menu_msg_type": "document"
    })    
