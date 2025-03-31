"""
Callbacks Router for Button Logic 🧠

Routes based on callback `data` to modularized handlers in `handlers/sections/`

handlers/
├── callbacks.py          # ← You're here
└── sections/
    ├── menu.py           # Handles "menu"
    ├── about.py          # Handles "about"
    ├── ecosystem.py      # Handles "ecosystem"
    ├── ecosystem_items.py# Handles "kendu_*"
    ├── buy.py            # Handles "buy_*", "how_to_*"
    ├── faq.py            # Handles "faq*"
    ├── contracts.py      # Handles "contract_addresses"
    └── follow.py         # Handles "follow_links"
"""

from telegram import Update
from telegram.ext import ContextTypes

from handlers.sections.menu import handle_menu
from handlers.sections.about import handle_about
from handlers.sections.ecosystem import handle_ecosystem
from handlers.sections.ecosystem_items import handle_ecosystem_item
from handlers.sections.buy import handle_buy
from handlers.sections.faq import handle_faq
from handlers.sections.contracts import handle_contracts
from handlers.sections.follow import handle_follow


async def handle_button(update: Update = None, context: ContextTypes.DEFAULT_TYPE = None, data_override=None, message_override=None):
    query = update.callback_query if update else None
    data = query.data if query else data_override
    message = query.message if query else message_override
    chat_id = message.chat_id

    if query:
        await query.answer()

    # Route to the appropriate section
    if data == "menu":
        await handle_menu(context, chat_id, message)
    elif data == "about":
        await handle_about(context, chat_id, message)
    elif data == "ecosystem":
        await handle_ecosystem(context, chat_id)
    elif data.startswith("kendu_"):
        await handle_ecosystem_item(context, chat_id, data)
    elif data.startswith("buy_") or data.startswith("how_to_"):
        await handle_buy(context, chat_id, data)
    elif data.startswith("faq"):
        await handle_faq(context, chat_id, data)
    elif data == "contract_addresses":
        await handle_contracts(context, chat_id, message)
    elif data == "follow_links":
        await handle_follow(context, chat_id, message)
    else:
        # Fallback
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        from utils.message_tools import smart_send_or_edit

        text = "⚠️ Unknown command. Please use /menu to get back to the main screen."
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🤖 Back to Menu", callback_data="menu")]
        ])
        await smart_send_or_edit(
            query=query,
            context=context,
            new_text=text,
            reply_markup=reply_markup,
            message_override=message_override
        )
