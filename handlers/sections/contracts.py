from telegram import Update
from telegram.ext import ContextTypes
from ui.menu_renderer import menu_renderer
from ui.menu_ui import get_contracts_text_and_markup
from core.menu_state import should_skip_section_render

async def handle_contract_addresses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await should_skip_section_render(update, context, section_type="text", section_key="contracts"):
        return

    print("📜 Contracts menu opened")

    text, reply_markup = get_contracts_text_and_markup()

    await menu_renderer(
        update=update,
        context=context,
        msg_type="text",
        text=text,
        reply_markup=reply_markup,
        section_key="contracts"
    )