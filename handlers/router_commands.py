from telegram.ext import CommandHandler
from core.message_tracker import wrap_command_handler

from handlers.sections.menu import handle_menu
from handlers.sections.about import handle_about
from handlers.sections.ecosystem import handle_ecosystem
from handlers.sections.buy import handle_buy_kendu
from handlers.sections.contracts import handle_contract_addresses
from handlers.sections.faq import handle_faq_menu
from handlers.sections.follow import handle_follow_links
from handlers.sections.price import handle_price  # ✅ NEW

from handlers.menu_actions import handle_start, logout, ask_restart_confirmation
from handlers.admin import refresh_commands

from core.commands_config import COMMAND_DEFINITIONS  # ✅ now clean


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
        "price": handle_price,  # ✅ NEW
        "logout": logout,
        "restart": ask_restart_confirmation,
    }

    for cmd, handler in command_handlers.items():
        bot_app.add_handler(CommandHandler(cmd, wrap_command_handler(handler)))

    # 🛠️ Dev/admin tools (unwrapped)
    bot_app.add_handler(CommandHandler("refreshcommands", refresh_commands))
