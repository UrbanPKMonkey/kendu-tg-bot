from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.menu_handler import menu_handler

# List of commands you want to display in the menu
ALL_COMMANDS = [
    "/start", "/menu", "/about", "/eco", "/buykendu", "/contracts", "/faq", "/follow", "/logout", "/restart"
]

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /menu command or Menu button tap."""
    print("📲 /menu or Menu button tapped — rendering main menu")

    text = (
        "🤖 <b>Kendu Main Menu</b>\n\n"
        "Tap an option below to explore:"
    )

    # Define menu buttons
    buttons = [
        [InlineKeyboardButton("🧠 About", callback_data="about")],
        [InlineKeyboardButton("🌐 Ecosystem", callback_data="ecosystem")],
        [InlineKeyboardButton("💰 Buy Kendu", callback_data="buy_kendu")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("🧾 Contract Addresses", callback_data="contract_addresses")],
        [InlineKeyboardButton("🔗 Follow", callback_data="follow_links")],
        [InlineKeyboardButton("💬 /commands", callback_data="show_commands")]  # New button for commands
    ]

    # Create inline keyboard with buttons
    reply_markup = InlineKeyboardMarkup(buttons)

    # Send the main menu
    await menu_handler(
        update=update,
        context=context,
        msg_type="text",
        text=text,
        reply_markup=reply_markup
    )


async def handle_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /commands callback and shows all available commands."""
    print("📜 /commands tapped — showing all available commands")

    # Create buttons for all commands
    buttons = [[InlineKeyboardButton(cmd, callback_data=cmd)] for cmd in ALL_COMMANDS]

    # Create the reply markup with command buttons
    reply_markup = InlineKeyboardMarkup(buttons)

    # Send the message with all commands
    await menu_handler(
        update=update,
        context=context,
        msg_type="text",
        text="Here are all the available commands:",
        reply_markup=reply_markup
    )
