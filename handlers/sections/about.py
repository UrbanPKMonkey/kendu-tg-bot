from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.menu_state import should_skip_section_render
from ui.menu_renderer import menu_renderer

async def handle_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await should_skip_section_render(update, context, section_type="text", section_key="about"):
        return

    print("🧠 About menu opened")

    text = (
        "🧠 <b>About Kendu</b>\n\n"
        "Kendu is a movement that empowers you to turn your life goals into reality.\n"
        "Take initiative, and the community will fuel your journey.\n\n"
        "<b>What is your dream? 💭</b>\n\n"
        "Choose a section to learn more 👇"
    )

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Power to the Holders", callback_data="about_holders")],
        [InlineKeyboardButton("🧱 For the Builders", callback_data="about_builders")],
        [InlineKeyboardButton("🌍 Bringing Crypto IRL", callback_data="about_irl")],
        [InlineKeyboardButton("📣 Community Building", callback_data="about_community")],
        [InlineKeyboardButton("🎥 Kendu Man Saves DeFi", callback_data="about_kendumanchad")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu")]
    ])

    await menu_renderer(
        update=update,
        context=context,
        msg_type="text",
        text=text,
        reply_markup=reply_markup,
        section_key="about"
    )