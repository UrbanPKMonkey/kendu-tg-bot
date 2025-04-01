from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from handlers.callbacks import handle_button
from handlers.sections.start import send_start_welcome_screen
from utils.menu_handler import menu_handler
from utils.menu_tools import (
    reset_menu_context,
    get_tracked_menu_state,
    safe_delete_message,
)
from utils.user_state import _reset_user_state
from utils.message_tools import track_bot_message  # ✅ NEW

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

# ===== /start handler with smart wipe prompt =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ /start received")

    # Clean up menu state, don't delete the /start message
    reset_menu_context(context)
    print("🔁 Menu context reset")

    tracked = context.user_data.get("menu_msg_ids", [])

    if len(tracked) > 1:
        print("🧼 Offering wipe or continue option...")
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
            text="<b>Welcome to the Official Kendu Bot</b>\n\nWould you like to start fresh by wiping the bot's message history?\n\nChoose below 👇",
            reply_markup=reply_markup
        )
        if hasattr(sent, "message_id"):
            context.user_data["menu_start_msg_id"] = sent.message_id
    else:
        print("🤖 No previous messages. Going straight to start page.")
        await send_start_welcome_screen(update, context)


# ===== Slash Command Routing =====
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE): await _route_command(update, context, "menu")
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE): await _route_command(update, context, "about")
async def eco(update: Update, context: ContextTypes.DEFAULT_TYPE): await _route_command(update, context, "eco")
async def buykendu(update: Update, context: ContextTypes.DEFAULT_TYPE): await _route_command(update, context, "buykendu")
async def contracts(update: Update, context: ContextTypes.DEFAULT_TYPE): await _route_command(update, context, "contracts")
async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE): await _route_command(update, context, "faq")
async def follow(update: Update, context: ContextTypes.DEFAULT_TYPE): await _route_command(update, context, "follow")


# ===== Unified Slash → Button Routing Core =====
async def _route_command(update: Update, context: ContextTypes.DEFAULT_TYPE, cmd_key: str):
    print(f"📩 /{cmd_key} command received")

    callback_data = ROUTES.get(cmd_key)
    if callback_data:
        await handle_button(update, context, data_override=callback_data)


# ===== Logout & Restart Commands =====
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("👋 /logout received")
    await _reset_user_state(update, context, reset_start=True)

    sent = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="✅ You’ve been logged out. Start again with /start or /menu.",
        parse_mode="HTML"
    )
    track_bot_message(context, sent)  # ✅


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("⚠️ /restart received — showing confirmation")

    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔁 Confirm Restart", callback_data="restart_confirmed"),
            InlineKeyboardButton("❌ Cancel", callback_data="restart_cancelled")
        ]
    ])

    sent = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="⚠️ <b>Are you sure you want to restart?</b>\n\nThis will wipe your current state and reinitialize the bot.",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    track_bot_message(context, sent)  # ✅
