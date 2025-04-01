from telegram.ext import CommandHandler

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
    """Register all slash commands with the bot."""
    bot_app.add_handler(CommandHandler("start", handle_start))
    bot_app.add_handler(CommandHandler("menu", handle_menu))
    bot_app.add_handler(CommandHandler("about", handle_about))
    bot_app.add_handler(CommandHandler("eco", handle_ecosystem))
    bot_app.add_handler(CommandHandler("buykendu", handle_buy_kendu))
    bot_app.add_handler(CommandHandler("contracts", handle_contract_addresses))
    bot_app.add_handler(CommandHandler("faq", handle_faq_menu))
    bot_app.add_handler(CommandHandler("follow", handle_follow_links))
    bot_app.add_handler(CommandHandler("logout", logout))
    bot_app.add_handler(CommandHandler("restart", ask_restart_confirmation))