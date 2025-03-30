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

    Parameters:
        query (CallbackQuery): When triggered by a button.
        context: Telegram context object.
        new_text (str): Message content.
        reply_markup (InlineKeyboardMarkup): Optional buttons.
        parse_mode (str): HTML/Markdown.
        message_override (Message): Used for slash commands.
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

    if old_msg_id:
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
            # Editing failed (e.g. media vs. text), try delete
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=old_msg_id)
            except Exception:
                pass  # Message already deleted or expired

    sent = await message.reply_text(
        text=new_text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )
    context.user_data["menu_msg_id"] = sent.message_id


async def add_black_background_to_image(image_url: str) -> BytesIO:
    """
    Adds a black background behind transparent PNGs for Telegram compatibility.

    Parameters:
        image_url (str): URL to the image.

    Returns:
        BytesIO: Image file ready to send.
    """
    response = requests.get(image_url)
    original = Image.open(BytesIO(response.content)).convert("RGBA")

    background = Image.new("RGB", original.size, (0, 0, 0))
    background.paste(original, mask=original.split()[3])  # Apply alpha channel

    output = BytesIO()
    output.name = "with_black_bg.png"
    background.save(output, format="PNG")
    output.seek(0)
    return output


def get_contracts_text_and_markup():
    """
    Returns contract text + back button markup.

    Returns:
        Tuple[str, InlineKeyboardMarkup]
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
