# handlers/sections/contracts.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.menu_handler import menu_handler
from utils.message_tools import get_contracts_text_and_markup, smart_send_or_edit


async def handle_contract_addresses(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    update: Update = None,
):
    # Skip if already showing
    if await menu_handler(context, chat_id, update, current_type="text"):
        return

    text, reply_markup = get_contracts_text_and_markup()

    await smart_send_or_edit(
        context=context,
        query=update.callback_query if update else None,
        new_text=text,
        reply_markup=reply_markup,
        message_override=update.message if update else None,
    )

    context.user_data["menu_msg_type"] = "text"
