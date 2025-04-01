# handlers/sections/ecosystem.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.menu_handler import menu_handler

async def handle_ecosystem(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message):
    # Skip if already showing the same text menu
    if await menu_handler(context, chat_id, message, current_type="text"):
        return

    text = (
        "🌐 <b>Kendu Ecosystem</b>\n\n"
        "Kendu is more than a token —\n"
        "It’s a <b>permissionless, decentralized brand</b> with no limits on what can be built.\n\n"
        "The community has already turned belief into:\n"
        "• Real products\n"
        "• Community businesses\n"
        "• Viral content\n\n"
        "<b>Kendu is your launchpad</b> for whatever comes next.\n"
        "If you can dream it, you can build it. 💥\n\n"
        "Explore our Ecosystem 👇"
    )

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ Kendu Energy Drink", callback_data="kendu_energy")],
        [InlineKeyboardButton("☕ Kendu Coffee", callback_data="kendu_coffee")],
        [InlineKeyboardButton("🎨 Kendu Creator", callback_data="kendu_creator")],
        [InlineKeyboardButton("🧢 Kendu Style", callback_data="kendu_style")],
        [InlineKeyboardButton("🧵 Kendu Unstitched", callback_data="kendu_unstitched")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu")]
    ])

    sent = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    context.user_data["menu_msg_id"] = sent.message_id
    context.user_data["menu_msg_type"] = "text"
