from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from core.menu_state import delete_all_bot_messages
from core.message_tracker import track_bot_message
from core.user_state import _reset_user_state
from ui.menu_renderer import menu_renderer


async def start_wipe_confirmed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🧼 Start wipe confirmed")
    await delete_all_bot_messages(update, context)
    await _reset_user_state(update, context, reset_start=True)
    await send_start_welcome_screen(update, context)


async def start_continue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🤖 Start without wipe")
    await _reset_user_state(update, context, reset_start=True)
    await send_start_welcome_screen(update, context)


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
    track_bot_message(context, sent)


async def restart_cancelled(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("❌ Restart cancelled")
    await _reset_user_state(update, context, reset_start=False)

    from handlers.router_callbacks import handle_button
    await handle_button(update, context, data_override="menu")


async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🚪 User logged out")
    await delete_all_bot_messages(update, context)
    await _reset_user_state(update, context, reset_start=True)

    sent = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="👋 You’ve been logged out.\nType /start to begin again or /menu to continue.",
        parse_mode="HTML"
    )
    track_bot_message(context, sent)


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
        "⚫ <b>Ethereum (ETH):</b>\n<code>0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18</code>\n\n"
        "🟣 <b>Solana (SOL):</b>\n<code>2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45</code>\n\n"
        "🔵 <b>Base (BASE):</b>\n<code>0xef73611F98DA6E57e0776317957af61B59E09Ed7</code>\n\n"
        "✅ <i><a href='https://skynet.certik.com/projects/kendu-inu'>CertiK</a> audit completed</i>\n\n"
        "Made with ❤️ by the Kendu Community."
    )

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 Menu", callback_data="menu")]
    ])

    sent = await menu_renderer(
        update=update,
        context=context,
        msg_type="photo",
        photo="https://i.imgur.com/r0i7fuG.png",
        text=caption,
        reply_markup=reply_markup
    )

    if hasattr(sent, "message_id"):
        context.user_data["menu_start_msg_id"] = sent.message_id
        print(f"✅ Tracked welcome image message: {sent.message_id}")
    else:
        print("⚠️ Failed to track welcome image message.")
