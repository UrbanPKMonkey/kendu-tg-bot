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


def register_slash_commands(bot_app):
    """Register all slash commands with the bot (with cleanup)."""
    commands = [
        ("start", handle_start),
        ("menu", handle_menu),
        ("about", handle_about),
        ("eco", handle_ecosystem),
        ("buykendu", handle_buy_kendu),
        ("contracts", handle_contract_addresses),
        ("faq", handle_faq_menu),
        ("follow", handle_follow_links),
        ("logout", logout),
        ("restart", ask_restart_confirmation),
    ]

    for cmd, handler in commands:
        bot_app.add_handler(CommandHandler(cmd, wrap_command_handler(handler)))
