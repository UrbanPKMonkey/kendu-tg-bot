from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from core.user_state import _reset_user_state
from core.message_tracker import track_bot_message
from ui.menu_renderer import menu_renderer
from handlers.sections.start import send_start_welcome_screen

from core.menu_state import delete_all_bot_messages, reset_menu_context


# === 🧼 /start: Wipe Confirmed ===
async def start_wipe_confirmed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🧼 Start wipe confirmed")
    await delete_all_bot_messages(update, context)
    await reset_menu_context(context)
    await _reset_user_state(update, context, reset_start=True)
    await send_start_welcome_screen(update, context)


# === 🤖 /start: Continue Without Wipe ===
async def start_continue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🤖 Start without wipe")
    await _reset_user_state(update, context, reset_start=True)
    await send_start_welcome_screen(update, context)


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
    await reset_menu_context(context)
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

    # Simulate return to menu
    from handlers.sections.menu import handle_menu
    await handle_menu(update, context)


# === 🔓 /logout — clears menu state only ===
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🔓 Logout command triggered")

    await reset_menu_context(context)

    sent = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="👋 You’ve been logged out of the current menu session.\nUse /menu to resume.",
        parse_mode="HTML"
    )
    track_bot_message(context, sent)
