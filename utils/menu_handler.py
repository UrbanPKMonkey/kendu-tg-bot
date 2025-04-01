# utils/menu_handler.py

from telegram import Message
from telegram.ext import ContextTypes

async def menu_handler(context: ContextTypes.DEFAULT_TYPE, chat_id: int, new_text: str, reply_markup, message: Message = None):
    """
    Universal menu handler to avoid duplicates and control deletion.
    If current message matches active menu, do nothing.
    """
    current_id = context.user_data.get("menu_msg_id")
    current_type = context.user_data.get("menu_msg_type", "text")

    # 1. If current menu is already shown, don't send again
    if message and message.message_id == current_id and current_type == "text":
        print("🛑 Menu already showing. Skipping duplicate send.")
        return

    # 2. Delete the old tracked menu message (if exists and not a photo)
    if current_id:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=current_id)
        except Exception:
            pass

    # 3. Delete the triggering message if it's not the main menu (i.e. slash command or button)
    try:
        if message and not message.photo:
            await message.delete()
    except Exception:
        pass

    # 4. Send fresh menu message
    sent = await context.bot.send_message(
        chat_id=chat_id,
        text=new_text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    context.user_data["menu_msg_id"] = sent.message_id
    context.user_data["menu_msg_type"] = "text"
