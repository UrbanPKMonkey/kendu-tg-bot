from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.user_state import _reset_user_state
from core.message_tracker import track_bot_message
from core.menu_state import delete_all_bot_messages, reset_menu_context
from ui.menu_renderer import menu_renderer

from handlers.sections.start import send_start_welcome_screen
from handlers.sections.menu import handle_menu


# === 🧼 /start: Wipe Confirmed ===
async def start_wipe_confirmed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🧼 Start wipe confirmed")
    await delete_all_bot_messages(update, context)
    reset_menu_context(context)
    await _reset_user_state(update, context, reset_start=True)
    await send_start_welcome_screen(update, context)


# === 🤖 /start: Continue Without Wipe ===
async def start_continue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🤖 Start without wipe")
    await _reset_user_state(update, context, reset_start=True)
    await send_start_welcome_screen(update, context)


# === 🔁 /restart: Ask for Confirmation ===
async def ask_restart_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Shows restart confirmation with Cancel + Confirm buttons."""

    text = (
        "⚠️ <b>Are you sure you want to fully restart?</b>\n\n"
        "This will wipe all menus, reset your session, and return to the welcome screen."
    )

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🧼 Restart & Wipe Everything", callback_data="restart_confirmed")],
        [InlineKeyboardButton("❌ Cancel", callback_data="restart_cancelled")]
    ])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )


# === 🔁 /restart: Confirmed Reset ===
async def restart_confirmed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ Restart confirmed")

    try:
        if update.callback_query:
            await update.callback_query.message.delete()
        if update.message:
            await update.message.delete()
    except Exception as e:
        print(f"⚠️ Failed to delete restart messages: {e}")

    await delete_all_bot_messages(update, context)
    reset_menu_context(context)
    await _reset_user_state(update, context, reset_start=True)

    sent = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🔁 Restart complete.\nUse /start to begin fresh or /menu to resume.",
        parse_mode="HTML"
    )
    track_bot_message(context, sent)


# === ❌ /restart: Cancelled ===
async def restart_cancelled(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("❌ Restart cancelled")
    await _reset_user_state(update, context, reset_start=False)
    await handle_menu(update, context)


# === 🔓 /logout — clears menu state only ===
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🔓 Logout command triggered")

    reset_menu_context(context)

    sent = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="👋 You’ve been logged out of the current menu session.\nUse /menu to resume.",
        parse_mode="HTML"
    )
    track_bot_message(context, sent)


# === 📜 /commands Inline Button ===
async def handle_show_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /commands button click to show available commands."""
    commands_text = (
        "📝 <b>Available Commands</b>\n\n"
        "/start     → Welcome screen\n"
        "/menu      → Open the main menu\n"
        "/about     → Learn about Kendu\n"
        "/eco       → Explore the Ecosystem\n"
        "/buykendu  → How to Buy\n"
        "/contracts → View Contract Addresses\n"
        "/faq       → Questions & Answers\n"
        "/follow    → Official Links & Socials\n"
        "/logout    → Clear menu state and reset\n"
        "/restart   → Full reset & reinit the bot"
    )

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="menu")]
    ])

    await menu_renderer(
        update=update,
        context=context,
        msg_type="text",
        text=commands_text,
        reply_markup=reply_markup,
        section_key="commands"
    )


# === 🚀 /start entry point ===
async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initial /start command — show wipe or continue only if messages exist."""
    user_data = context.user_data
    menu_msg_ids = user_data.get("menu_msg_ids", [])
    has_existing = len(menu_msg_ids) > 0

    if has_existing:
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🧼 Start Fresh (Wipe Chat History)", callback_data="start_wipe_confirmed")],
            [InlineKeyboardButton("📲 Continue Without Deleting", callback_data="start_continue")]
        ])

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="👋 Welcome back!\n\nWould you like to start fresh or continue?",
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    else:
        await start_continue(update, context)
