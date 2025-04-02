from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.price_fetcher import get_kendu_price_panel
from ui.menu_renderer import menu_renderer


async def handle_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📊 /price command triggered")
    context.user_data["current_section"] = "price"

    price_panel = await get_kendu_price_panel()

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Refresh Price", callback_data="refresh_prices")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu")]
    ])

    await menu_renderer(
        update=update,
        context=context,
        msg_type="text",
        text=price_panel,
        reply_markup=reply_markup,
        section_key="price"
    )
