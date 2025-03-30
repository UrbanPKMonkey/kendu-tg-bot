from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.callbacks import handle_button


# Reuse from message_tools if needed (e.g., for contracts)
from utils.message_tools import get_contracts_text_and_markup


# 🔁 Helper: simulate callback button press from slash commands
def make_fake_query(update: Update, data: str):
    return type("FakeQuery", (), {
        "data": data,
        "message": update.message,
        "answer": lambda: None
    })()


# ✅ /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🤖 Menu", callback_data="menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo="https://i.imgur.com/r0i7fuG.png",
        caption=(
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
        ),
        parse_mode="HTML",
        reply_markup=reply_markup
    )


# ✅ /menu command
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fake_query = make_fake_query(update, "menu")
    await handle_button(fake_query, context)


# ✅ /about command
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fake_query = make_fake_query(update, "about")
    await handle_button(fake_query, context)


# ✅ /eco command
async def eco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fake_query = make_fake_query(update, "ecosystem")
    await handle_button(fake_query, context)


# ✅ /buykendu command
async def buykendu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fake_query = make_fake_query(update, "buy_kendu")
    await handle_button(fake_query, context)


# ✅ /contracts command
async def contracts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fake_query = make_fake_query(update, "contract_addresses")
    await handle_button(fake_query, context)


# ✅ /faq command
async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fake_query = make_fake_query(update, "faq")
    await handle_button(fake_query, context)


# ✅ /follow command
async def follow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fake_query = make_fake_query(update, "follow_links")
    await handle_button(fake_query, context)
