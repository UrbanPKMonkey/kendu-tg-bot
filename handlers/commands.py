from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.callbacks import handle_button
from utils.menu_handler import menu_handler

# ===== Shared: Route map for slash commands → callback buttons =====
ROUTES = {
    "menu": "menu",
    "about": "about",
    "eco": "ecosystem",
    "buykendu": "buy_kendu",
    "contracts": "contract_addresses",
    "faq": "faq",
    "follow": "follow_links",
}


# ===== /start handler (Welcome image with tracked menu cleanup) =====
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


# ===== Unified slash command dispatcher =====
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _route_command(update, context, "menu")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _route_command(update, context, "about")

async def eco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _route_command(update, context, "eco")

async def buykendu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _route_command(update, context, "buykendu")

async def contracts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _route_command(update, context, "contracts")

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _route_command(update, context, "faq")

async def follow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _route_command(update, context, "follow")


# ===== Shared command routing logic =====
async def _route_command(update: Update, context: ContextTypes.DEFAULT_TYPE, cmd_key: str):
    print(f"📩 /{cmd_key} command received")

    if await menu_handler(update, context, msg_type="text"):
        return

    callback_data = ROUTES.get(cmd_key)
    if callback_data:
        await handle_button(update, context, data_override=callback_data)
