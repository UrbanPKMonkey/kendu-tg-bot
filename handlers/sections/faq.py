# handlers/sections/faq.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.menu_handler import menu_handler


async def handle_faq_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "❓ <b>Frequently Asked Questions</b>\n\n"
        "Choose a question below to view the answer:"
    )

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔸 What is Kendu?", callback_data="faq_what_is_kendu")],
        [InlineKeyboardButton("🐕 Is Kendu just another dog token?", callback_data="faq_is_dog_token")],
        [InlineKeyboardButton("🚀 What will take Kendu to the next level?", callback_data="faq_next_level")],
        [InlineKeyboardButton("🙋 How can I help?", callback_data="faq_help")],
        [InlineKeyboardButton("📈 When are we reaching ___ market cap?", callback_data="faq_marketcap")],
        [InlineKeyboardButton("📉 Why is Kendu dipping/pumping?", callback_data="faq_dipping")],
        [InlineKeyboardButton("🛡️ How can I keep my tokens safe?", callback_data="faq_safety")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu")]
    ])

    await menu_handler(update, context, msg_type="text", text=text, reply_markup=reply_markup)


async def handle_faq_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
    faq_data = {
        "faq_what_is_kendu": (
            "🔸 <b>What is Kendu?</b>\n\n"
            "Kendu is a memecoin ecosystem and social movement led and driven forward by its community through organic effort. "
            "We don't engage in paid marketing or fake engagement — everything comes from consistent daily action. "
            "The more we activate, the faster Kendu rises. This is a masterclass in scaling through real conviction. 🚀"
        ),
        "faq_is_dog_token": (
            "🐕 <b>Is Kendu just another dog/animal token?</b>\n\n"
            "Nope. The name and logo symbolize loyalty and tenacity, not memetic fluff. "
            "Kendu is original IP with deep roots and a builder-first culture. This isn’t a gimmick. It’s a mission."
        ),
        "faq_next_level": (
            "🚀 <b>What will take Kendu to the next level?</b>\n\n"
            "You. Your posts, your voice, your energy. Kendu scales with people who activate. "
            "No matter your skill set — your impact is exponential if you show up daily and inspire others to join."
        ),
        "faq_help": (
            "🙋 <b>How can I help?</b>\n\n"
            "Post, reply, share. Onboard friends. Rep IRL. Talk about Kendu on X, TikTok, Reddit, YouTube. "
            "Be creative and respectful. This is a collective effort — be part of the reason we make it."
        ),
        "faq_marketcap": (
            "📈 <b>When are we reaching ___ market cap?</b>\n\n"
            "There's no set date. The pace is set by the community's daily energy. "
            "If we scale our activity, the chart will follow. This is programmed growth — powered by us."
        ),
        "faq_dipping": (
            "📉 <b>Why is Kendu dipping/pumping?</b>\n\n"
            "Markets breathe. Ups and downs are normal. Redistribution strengthens conviction. "
            "Zoom out. Focus on community health and long-term culture, not short-term candles."
        ),
        "faq_safety": (
            "🛡️ <b>How can I keep my tokens safe?</b>\n\n"
            "• Never share your seed phrase\n"
            "• Use hardware or trusted wallets\n"
            "• Double-check URLs before connecting\n"
            "• Kendu will never DM or offer airdrops\n"
            "Stay safe, stay vigilant!"
        )
    }

    if data not in faq_data:
        return

    text = faq_data[data]
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="faq")]
    ])

    await menu_handler(update, context, msg_type="text", text=text, reply_markup=reply_markup)
