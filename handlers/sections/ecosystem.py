# handlers/sections/ecosystem.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def handle_ecosystem(update: Update = None, context: ContextTypes.DEFAULT_TYPE = None, query=None, message_override=None):
    """Displays the Kendu Ecosystem section."""
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

    chat_id = (query.message.chat_id if query else message_override.chat_id)

    # Always delete previous tracked menu message if it exists
    old_msg_id = context.user_data.get("menu_msg_id")
    try:
        if old_msg_id:
            await context.bot.delete_message(chat_id=chat_id, message_id=old_msg_id)
    except Exception:
        pass

    # Send fresh message
    sent = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    # Track new menu message
    context.user_data["menu_msg_id"] = sent.message_id
    context.user_data["menu_msg_type"] = "text"
