from telegram import InlineKeyboardMarkup, Message
from telegram.ext import ContextTypes

async def smart_send_or_edit(
    query,
    context: ContextTypes.DEFAULT_TYPE,
    new_text: str,
    reply_markup: InlineKeyboardMarkup
):
    """
    Edits a message if it's text, deletes and sends new if it's media (like photo).
    """
    if query.message.photo:
        await query.message.delete()
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=new_text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    else:
        await query.message.edit_text(
            text=new_text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
