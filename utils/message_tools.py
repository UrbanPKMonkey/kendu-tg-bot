from telegram import InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import ContextTypes


async def smart_send_or_edit(
    query,
    context: ContextTypes.DEFAULT_TYPE,
    new_text: str,
    reply_markup: InlineKeyboardMarkup = None,
    parse_mode: str = "HTML"
):
    """Edits the existing menu message or deletes & sends a new one if not editable."""
    chat_id = query.message.chat_id
    old_msg_id = context.user_data.get("menu_msg_id")

    # If we already have a stored message ID
    if old_msg_id:
        try:
            # Try to edit the existing message
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=old_msg_id,
                text=new_text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
            return  # Success ✅
        except Exception as e:
            # If it fails (e.g. message was a photo), delete it and send new
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=old_msg_id)
            except Exception:
                pass  # Ignore if already deleted

    # Send a new text message (used if there’s no msg_id or edit failed)
    sent = await query.message.reply_text(
        text=new_text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )
    context.user_data["menu_msg_id"] = sent.message_id

from PIL import Image
import requests
from io import BytesIO

async def add_black_background_to_image(image_url: str) -> BytesIO:
    """
    Loads an image from URL, adds a black background if it has transparency,
    and returns a BytesIO object ready for Telegram upload.
    """
    response = requests.get(image_url)
    original = Image.open(BytesIO(response.content)).convert("RGBA")

    # Create black background the same size as original
    background = Image.new("RGB", original.size, (0, 0, 0))
    background.paste(original, mask=original.split()[3])  # Use alpha channel as mask

    output = BytesIO()
    output.name = "with_black_bg.png"
    background.save(output, format="PNG")
    output.seek(0)
    return output