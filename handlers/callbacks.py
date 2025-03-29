from telegram import Update
from telegram.ext import ContextTypes

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    responses = {
        "shop_merch": "🛍 Welcome to the merch store! Coming soon.",
        "buy_crypto": "💰 Ready to buy crypto? Coming soon.",
        "view_history": "📜 Viewing your purchase history... coming soon.",
        "social_links": "🔗 Socials:\nTwitter: ...\nReddit: ...\nDiscord: ..."
    }

    await query.edit_message_text(responses.get(data, "❌ Unknown action."))
