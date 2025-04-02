from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# 🔧 Core utilities
from core.message_tracker import track_bot_message
from ui.menu_renderer import menu_renderer

# 📚 Section handlers
from handlers.sections.menu import handle_menu
from handlers.sections.about import handle_about
from handlers.sections.ecosystem import handle_ecosystem
from handlers.sections.ecosystem_items import handle_ecosystem_item
from handlers.sections.buy import handle_buy_kendu, handle_buy_chain, handle_refresh_prices
from handlers.sections.faq import handle_faq_menu, handle_faq_answer
from handlers.sections.contracts import handle_contract_addresses
from handlers.sections.follow import handle_follow_links
from handlers.sections.price import handle_price  # ✅ Confirmed updated

# 🚀 Action callbacks
from handlers.menu_actions import (
    start_wipe_confirmed,
    start_continue,
    restart_confirmed,
    restart_cancelled
)

# === 🧠 Central Callback Router ===
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE, data_override=None):
    query = update.callback_query if update else None
    data = query.data if query else data_override

    if query:
        await query.answer()

    # 🔀 Routing based on callback data
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

    elif data.startswith(("buy_", "how_to_")):
        await handle_buy_chain(update, context, data)

    elif data == "refresh_prices":
        await handle_refresh_prices(update, context)

    elif data == "price":
        await handle_price(update, context)

    elif data == "faq":
        await handle_faq_menu(update, context)

    elif data.startswith("faq_"):
        await handle_faq_answer(update, context, data)

    elif data == "contract_addresses":
        await handle_contract_addresses(update, context)

    elif data == "follow_links":
        await handle_follow_links(update, context)

    elif data == "start_wipe_confirmed":
        await start_wipe_confirmed(update, context)

    elif data == "start_continue":
        await start_continue(update, context)

    elif data == "restart_confirmed":
        await restart_confirmed(update, context)

    elif data == "restart_cancelled":
        await restart_cancelled(update, context)

    else:
        # ❌ Handle unknown buttons gracefully
        text = "⚠️ Unknown command. Please use /menu to return to the main menu."
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🤖 Back to Menu", callback_data="menu")]
        ])

        sent_message = await menu_renderer(
            update=update,
            context=context,
            msg_type="text",
            text=text,
            reply_markup=reply_markup
        )
        track_bot_message(context, sent_message)


# === 📜 /commands Inline Button Handler ===
async def handle_show_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays available slash commands clearly."""
    commands_text = (
        "📝 <b>Available Commands</b>\n\n"
        "/start     → Welcome screen\n"
        "/menu      → Open the main menu\n"
        "/about     → Learn about Kendu\n"
        "/eco       → Explore the Ecosystem\n"
        "/buykendu  → How to Buy\n"
        "/price     → Live Kendu Prices\n"
        "/contracts → View Contract Addresses\n"
        "/faq       → Questions & Answers\n"
        "/follow    → Official Links & Socials\n"
        "/logout    → Clear menu state and reset\n"
        "/restart   → Full reset & reinitialize bot"
    )

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="menu")]
    ])

    await menu_renderer(
        update=update,
        context=context,
        msg_type="text",
        text=commands_text,
        reply_markup=reply_markup
    )
