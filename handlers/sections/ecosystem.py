from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ui.menu_renderer import menu_renderer

async def handle_ecosystem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🌐 Ecosystem menu opened")

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

    await menu_renderer(
        update=update,
        context=context,
        msg_type="text",
        text=text,
        reply_markup=reply_markup
    )
    return
