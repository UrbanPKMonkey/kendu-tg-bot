# utils/simulate.py

from telegram import Update, Message
from telegram.ext import ContextTypes
from handlers.callbacks import handle_button


async def simulate_button(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
    print(f"🔁 simulate_button triggered with data: {data}")

    try:
        message = update.message if update and update.message else None

        await handle_button(
            update=None,
            context=context,
            data_override=data,
            message_override=message
        )

        if message:
            try:
                await message.delete()
            except Exception as e:
                print(f"⚠️ Failed to delete slash command message: {e}")

    except Exception as e:
        print(f"❌ simulate_button error for '{data}': {e}")