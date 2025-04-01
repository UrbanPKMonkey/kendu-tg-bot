from telegram.ext import CommandHandler
from core.message_tracker import wrap_command_handler  # 🧠 Unified handler wrapper

from handlers.sections.menu import handle_menu
from handlers.sections.about import handle_about
from handlers.sections.ecosystem import handle_ecosystem
from handlers.sections.buy import handle_buy_kendu
from handlers.sections.contracts import handle_contract_addresses
from handlers.sections.faq import handle_faq_menu
from handlers.sections.follow import handle_follow_links

# 🚀 Shared command actions
from handlers.menu_actions import handle_start, logout, ask_restart_confirmation

# 🛠️ Dev/Admin tools
from handlers.admin import refresh_commands


# 🌐 Centralized list for both slash registration + blue Telegram menu
COMMAND_DEFINITIONS = [
    ("start", "Start the bot and show welcome screen"),
    ("menu", "Open the main menu"),
    ("about", "Learn about Kendu"),
    ("eco", "Explore the Ecosystem"),
    ("buykendu", "How to Buy"),
    ("contracts", "View Contract Addresses"),
    ("faq", "Frequently Asked Questions"),
    ("follow", "Official Links & Socials"),
    ("logout", "Clear menu state and reset"),
    ("restart", "Full reset and start fresh"),
    # Optional: ("refreshcommands", "Force update Telegram command list") ← leave out of blue menu for now
]


def register_slash_commands(bot_app):
    """Register all slash commands with the bot (wrapped for cleanup)."""
    command_handlers = {
        "start": handle_start,
        "menu": handle_menu,
        "about": handle_about,
        "eco": handle_ecosystem,
        "buykendu": handle_buy_kendu,
        "contracts": handle_contract_addresses,
        "faq": handle_faq_menu,
        "follow": handle_follow_links,
        "logout": logout,
        "restart": ask_restart_confirmation,
    }

    for cmd, handler in command_handlers.items():
        bot_app.add_handler(CommandHandler(cmd, wrap_command_handler(handler)))

    # 🔧 Dev command (no wrapper for now)
    bot_app.add_handler(CommandHandler("refreshcommands", refresh_commands))
