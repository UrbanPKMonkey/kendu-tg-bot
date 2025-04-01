from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from core.menu_state import get_tracked_menu_state
from ui.menu_renderer import menu_renderer


async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 🧠 Prevent duplicate renders if the menu is already shown
    old_msg_ids, old_type = get_tracked_menu_state(context)
    if old_type == "text" and old_msg_ids:
        print("⏭️ Menu already active — skipping re-render")
        return

    print("📲 /menu or Menu button tapped — rendering main menu")

    text = (
        "<b>Welcome to the Kendu Ecosystem Menu</b>\n\n"
        "Explore the decentralized world of Kendu Inu:\n\n"
        "🧠 /about — What is Kendu?\n"
        "🌱 /eco — Our Ecosystem\n"
        "💰 /buykendu — How to Buy\n"
        "📄 /contracts — Contract Addresses\n"
        "❓ /faq — Questions & Answers\n"
        "🌐 /follow — Socials & Links\n\n"
        "Choose an option below 👇"
    )

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🧠 About", callback_data="about")],
        [InlineKeyboardButton("🌱 Ecosystem", callback_data="ecosystem")],
        [InlineKeyboardButton("💰 Buy Kendu", callback_data="buy_kendu")],
        [InlineKeyboardButton("📄 Contract Addresses", callback_data="contract_addresses")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("🌐 Follow Links", callback_data="follow_links")]
    ])

    await menu_renderer(
        update=update,
        context=context,
        msg_type="text",
        text=text,
        reply_markup=reply_markup
    )
