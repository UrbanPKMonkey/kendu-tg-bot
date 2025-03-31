from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.callbacks import handle_button
from utils.message_tools import delete_and_send_new

# ✅ Simulates a button tap from a slash command
async def simulate_button(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
    try:
        print(f"🔁 simulate_button triggered with data: {data}")
        await handle_button(
            update=None,
            context=context,
            data_override=data,
            message_override=update.message
        )
    except Exception as e:
        print(f"❌ simulate_button error for '{data}': {e}")

# ✅ /start command shows welcome image
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("✅ /start received")

    try:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🤖 Menu", callback_data="menu")]
        ])

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
            reply_markup=keyboard
        )

    except Exception as e:
        print(f"❌ Error in /start: {e}")

# ✅ Slash commands that DELETE before simulating buttons
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /menu command received")
    await delete_and_send_new(update, context, "⏳ Loading Menu…")
    await simulate_button(update, context, "menu")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /about command received")
    await delete_and_send_new(update, context, "⏳ Loading About…")
    await simulate_button(update, context, "about")

async def eco(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /eco command received")
    await delete_and_send_new(update, context, "⏳ Loading Ecosystem…")
    await simulate_button(update, context, "ecosystem")

async def buykendu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /buykendu command received")
    await delete_and_send_new(update, context, "⏳ Loading How to Buy…")
    await simulate_button(update, context, "buy_kendu")

async def contracts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /contracts command received")
    await delete_and_send_new(update, context, "⏳ Loading Contracts…")
    await simulate_button(update, context, "contract_addresses")

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /faq command received")
    await delete_and_send_new(update, context, "⏳ Loading FAQ…")
    await simulate_button(update, context, "faq")

async def follow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /follow command received")
    await delete_and_send_new(update, context, "⏳ Loading Socials…")
    await simulate_button(update, context, "follow_links")
