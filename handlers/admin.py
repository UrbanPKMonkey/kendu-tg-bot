# handlers/admin.py

from telegram import Update, BotCommand
from telegram.ext import ContextTypes

from core.commands_config import COMMAND_DEFINITIONS  # ✅ avoids circular import

# === 🔄 Refresh Telegram Slash Menu Commands ===
async def refresh_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = [BotCommand(cmd, desc) for cmd, desc in COMMAND_DEFINITIONS]
    await context.bot.set_my_commands(commands)
    await update.message.reply_text("🔄 Commands list refreshed and synced with Telegram!")

    print("📋 Blue Menu Commands updated:")
    for cmd in commands:
        print(f"• /{cmd.command} — {cmd.description}")
