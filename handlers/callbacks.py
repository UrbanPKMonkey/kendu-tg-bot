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

# handlers/callbacks.py

from telegram import Update
from telegram.ext import ContextTypes

from handlers.sections.menu import handle_menu
from handlers.sections.about import handle_about
from handlers.sections.ecosystem import handle_ecosystem
from handlers.sections.ecosystem_items import handle_ecosystem_item
from handlers.sections.buy import handle_buy_kendu, handle_buy_chain
from handlers.sections.faq import handle_faq_menu, handle_faq_answer
from handlers.sections.contracts import handle_contract_addresses
from handlers.sections.follow import handle_follow_links


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE, data_override=None):
    query = update.callback_query if update else None
    data = query.data if query else data_override

    if query:
        await query.answer()

    # Route to the appropriate section
    if data == "menu":
        await handle_menu(update, context)
    elif data == "about":
        await handle_about(update, context)
    elif data == "ecosystem":
        await handle_ecosystem(update, context)
    elif data.startswith("kendu_"):
        await handle_ecosystem_item(update, context, data)
    elif data == "buy_kendu":
        await handle_buy_kendu(update, context)
    elif data.startswith("buy_") or data.startswith("how_to_"):
        await handle_buy_chain(update, context, data)
    elif data == "faq":
        await handle_faq_menu(update, context)
    elif data.startswith("faq_"):
        await handle_faq_answer(update, context, data)
    elif data == "contract_addresses":
        await handle_contract_addresses(update, context)
    elif data == "follow_links":
        await handle_follow_links(update, context)
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
            reply_markup=reply_markup
        )