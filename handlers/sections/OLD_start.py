from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ui.menu_renderer import menu_renderer

async def send_start_welcome_screen(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends the welcome screen to the user when they start interacting with the bot.
    Offers options to explore Kendu's projects and ecosystem.
    """

    # Construct the welcome message
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

    # Create reply markup (button)
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🤖 Menu", callback_data="menu")]
    ])

    # Send the welcome message with image
    try:
        sent = await menu_renderer(
            update=update,
            context=context,
            msg_type="photo",
            photo="https://i.imgur.com/r0i7fuG.png",
            text=caption,
            reply_markup=reply_markup
        )

        if hasattr(sent, "message_id"):
            # Track the sent message for potential deletion/editing later
            context.user_data["menu_start_msg_id"] = sent.message_id
            print(f"✅ Tracked welcome image message: {sent.message_id}")
        else:
            print("⚠️ Failed to track welcome image message.")
    
    except Exception as e:
        print(f"❌ Error while sending welcome screen: {e}")
