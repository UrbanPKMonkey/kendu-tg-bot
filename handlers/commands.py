from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.callbacks import handle_button
from utils.message_tools import delete_and_send_new
from utils.menu_handler import menu_handler

# ✅ /start command shows welcome image (smart-tracked)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ /start received")

    caption = (
        "<b>Welcome to the Official Kendu Bot</b> — your all-in-one portal to the decentralized Kendu ecosystem.\n\n"
        "<b>We don’t gamble, we work.</b> 💪\n\n"
        "Explore the projects, get involved, and join the movement.\n\n"
        "﹎﹎﹎﹎﹎﹎﹎\n\n"
        "🤖 Tap /menu to get started or explore:\n\n"
        "/about     → What is Kendu?\n"
        "/eco       → Our Ecosystem\n"
        "/buykendu  → How to Buy\n"
        "/faq       → Questions & Answers\n"
        "/contracts → Contract Addresses\n"
        "/follow    → Socials & Links\n"
        "﹎﹎﹎﹎﹎﹎﹎\n\n"
        "<b>🌐 Official Website:</b> <a href='https://kendu.io'>https://kendu.io</a>\n"
        "<b>💬 Telegram:</b> <a href='https://t.me/Kendu'>https://t.me/Kendu</a>\n"
        "<b>📣 Twitter/X:</b> <a href='https://x.com/KenduInu'>https://x.com/KenduInu</a>\n"
        "<b>📰 Reddit:</b> <a href='https://www.reddit.com/r/KenduInu_Ecosystem'>r/KenduInu_Ecosystem</a>\n\n"
        "⛓️ Available on <b>Ethereum (ETH)</b>, <b>Solana (SOL)</b>, and <b>Base (BASE)</b>\n\n"
        "⚫ <b>Ethereum (ETH):</b>\n"
        "<code>   0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18</code>\n\n"
        "🟣 <b>Solana (SOL):</b>\n"
        "<code>   2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45</code>\n\n"
        "🔵 <b>Base (BASE):</b>\n"
        "<code>   0xef73611F98DA6E57e0776317957af61B59E09Ed7</code>\n\n"
        "✅ <i><a href='https://skynet.certik.com/projects/kendu-inu'>CertiK</a> audit completed</i>\n\n"
        "Made with ❤️ by the Kendu Community."
    )

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 Menu", callback_data="menu")]
    ])

    await menu_handler(
        update=update,
        context=context,
        msg_type="photo",
        photo="https://i.imgur.com/r0i7fuG.png",
        text=caption,
        reply_markup=reply_markup
    )

# ✅ Slash commands using new menu_handler (No simulate_button)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /menu command received")

    if await menu_handler(update, context, msg_type="text"):
        return  # Already showing correct menu

    await handle_button(update, context, data_override="menu")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /about command received")

    if await menu_handler(update, context, msg_type="text"):
        return

    await handle_button(update, context, data_override="about")

async def eco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /eco command received")

    if await menu_handler(update, context, msg_type="text"):
        return

    await handle_button(update, context, data_override="ecosystem")

async def buykendu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /buykendu command received")

    if await menu_handler(update, context, msg_type="text"):
        return

    await handle_button(update, context, data_override="buy_kendu")

async def contracts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /contracts command received")

    if await menu_handler(update, context, msg_type="text"):
        return

    await handle_button(update, context, data_override="contract_addresses")

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /faq command received")

    if await menu_handler(update, context, msg_type="text"):
        return

    await handle_button(update, context, data_override="faq")

async def follow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /follow command received")

    if await menu_handler(update, context, msg_type="text"):
        return

    await handle_button(update, context, data_override="follow_links")
