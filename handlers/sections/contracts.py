# handlers/sections/contracts.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.message_tools import get_contracts_text_and_markup, smart_send_or_edit


async def handle_contract_addresses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text, reply_markup = get_contracts_text_and_markup()

    await smart_send_or_edit(
        query=update.callback_query,
        context=context,
        new_text=text,
        reply_markup=reply_markup
    )
