from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# 🔧 Bot utilities
from utils.message_tools import (
    smart_send_or_edit,
    delete_all_bot_messages,
    track_bot_message  # ✅ NEW
)
from utils.menu_tools import (
    reset_menu_context,
    get_tracked_menu_state,
    safe_delete_message,
)
from utils.user_state import _reset_user_state

# 📚 Core section handlers
from handlers.sections.menu import handle_menu
from handlers.sections.about import handle_about
from handlers.sections.ecosystem import handle_ecosystem
from handlers.sections.ecosystem_items import handle_ecosystem_item
from handlers.sections.buy import handle_buy_kendu, handle_buy_chain
from handlers.sections.faq import handle_faq_menu, handle_faq_answer
from handlers.sections.contracts import handle_contract_addresses
from handlers.sections.follow import handle_follow_links
from handlers.sections.start import send_start_welcome_screen


# === 🧠 Central Callback Router ===
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE, data_override=None):
    query = update.callback_query if update else None
    data = query.data if query else data_override

    if query:
        await query.answer()

    # 🔀 Route by callback data
    if data == "menu":
        await handle_menu(update, context)
    elif data == "about":
        await handle_about(update, context)
    elif data == "ecosystem":
        await handle_ecosystem(update, context)
    elif data.startswith("kendu_"):
        await handle_ecosystem_item(update, context, data)
    elif data == "buy_kendu":
        await handle_buy_kendu(update, context)
    elif data.startswith("buy_") or data.startswith("how_to_"):
        await handle_buy_chain(update, context, data)
    elif data == "faq":
        await handle_faq_menu(update, context)
    elif data.startswith("faq_"):
        await handle_faq_answer(update, context, data)
    elif data == "contract_addresses":
        await handle_contract_addresses(update, context)
    elif data == "follow_links":
        await handle_follow_links(update, context)
    elif data == "start_wipe_confirmed":
        await start_wipe_confirmed(update, context)
    elif data == "start_continue":
        await start_continue(update, context)
    elif data == "restart_confirmed":
        await restart_confirmed(update, context)
    elif data == "restart_cancelled":
        await restart_cancelled(update, context)
    else:
        # ❌ Fallback for unknown buttons
        text = "⚠️ Unknown command. Please use /menu to get back to the main screen."
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🤖 Back to Menu", callback_data="menu")]
        ])
        sent = await smart_send_or_edit(
            query=query,
            context=context,
            new_text=text,
            reply_markup=reply_markup
        )
        track_bot_message(context, sent)  # ✅ Track fallback message


# === 🧼 /start: Wipe Confirmed ===
async def start_wipe_confirmed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🧼 Start wipe confirmed")
    await delete_all_bot_messages(update, context)
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
    await _reset_user_state(update, context, reset_start=True)

    sent = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🔁 Restart complete.\nUse /start to begin fresh or /menu to resume.",
        parse_mode="HTML"
    )
    track_bot_message(context, sent)  # ✅ Track the confirmation


# === ❌ /restart: Cancelled ===
async def restart_cancelled(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("❌ Restart cancelled")
    await _reset_user_state(update, context, reset_start=False)
    await handle_button(update, context, data_override="menu")
