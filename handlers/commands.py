from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.callbacks import handle_button
from utils.menu_handler import menu_handler
from utils.menu_tools import (
    reset_menu_context,
    get_tracked_menu_state,
    safe_delete_message,
)

# ===== Route map for slash commands → callback data =====
ROUTES = {
    "menu": "menu",
    "about": "about",
    "eco": "ecosystem",
    "buykendu": "buy_kendu",
    "contracts": "contract_addresses",
    "faq": "faq",
    "follow": "follow_links",
}

# ===== /start handler (welcome image and context reset) =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ /start received")

    await _reset_user_state(update, context, reset_start=True)

    caption = (
        "<b>Welcome to the Official Kendu Bot</b>\n\n"
        "Would you like to <b>start fresh</b> by wiping the bot's message history?\n\n"
        "Choose below 👇"
    )

    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🧼 Start Fresh (Wipe History)", callback_data="start_wipe_confirmed"),
            InlineKeyboardButton("🤖 Continue Without Deleting", callback_data="start_continue")
        ]
    ])

    sent = await menu_handler(
        update=update,
        context=context,
        msg_type="text",
        text=caption,
        reply_markup=reply_markup
    )

    if hasattr(sent, "message_id"):
        context.user_data["menu_start_msg_id"] = sent.message_id


async def send_start_welcome_screen(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    sent = await menu_handler(
        update=update,
        context=context,
        msg_type="photo",
        photo="https://i.imgur.com/r0i7fuG.png",
        text=caption,
        reply_markup=reply_markup
    )

    if hasattr(sent, "message_id"):
        context.user_data["menu_start_msg_id"] = sent.message_id


# ===== Slash Command Routing =====
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE): await _route_command(update, context, "menu")
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE): await _route_command(update, context, "about")
async def eco(update: Update, context: ContextTypes.DEFAULT_TYPE): await _route_command(update, context, "eco")
async def buykendu(update: Update, context: ContextTypes.DEFAULT_TYPE): await _route_command(update, context, "buykendu")
async def contracts(update: Update, context: ContextTypes.DEFAULT_TYPE): await _route_command(update, context, "contracts")
async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE): await _route_command(update, context, "faq")
async def follow(update: Update, context: ContextTypes.DEFAULT_TYPE): await _route_command(update, context, "follow")

# ===== Router Core =====
async def _route_command(update: Update, context: ContextTypes.DEFAULT_TYPE, cmd_key: str):
    print(f"📩 /{cmd_key} command received")

    callback_data = ROUTES.get(cmd_key)
    if callback_data:
        await handle_button(update, context, data_override=callback_data)


# ===== Logout & Restart Commands =====
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("👋 /logout received")
    await _reset_user_state(update, context, reset_start=True)  # 👈 force full reset
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="✅ You’ve been logged out. Start again with /start or /menu.",
        parse_mode="HTML"
    )

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🔁 /restart received")
    await _reset_user_state(update, context, reset_start=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🔁 Your session has been reset.\nUse /start to begin fresh or /menu to re-enter the portal.",
        parse_mode="HTML"
    )


# ===== Shared State Cleanup =====
async def _reset_user_state(update: Update, context: ContextTypes.DEFAULT_TYPE, reset_start=False):
    message = update.message or (update.callback_query and update.callback_query.message)
    chat_id = message.chat_id if message else None

    if not chat_id:
        print("⚠️ No chat_id found during reset")
        return

    old_msg_ids, _ = get_tracked_menu_state(context)
    preserved_id = context.user_data.get("menu_start_msg_id")

    for msg_id in old_msg_ids:
        if reset_start or msg_id != preserved_id:
            await safe_delete_message(context, chat_id, msg_id)

    if reset_start:
        context.user_data["menu_start_msg_id"] = None

    reset_menu_context(context)
