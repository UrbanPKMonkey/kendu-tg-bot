# handlers/sections/faq.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from handlers.sections.menu import edit_menu_response


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

    msg_id = context.user_data.get("menu_msg_id")
    if msg_id:
        await edit_menu_response(context, update.effective_chat.id, msg_id, text, reply_markup)


async def handle_faq_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, question_id: str):
    answers = {
        "faq_what_is_kendu": (
            "🔸 <b>What is Kendu?</b>\n\n"
            "Kendu is a memecoin ecosystem and movement powered by autonomous community action — no bots, no market makers, no fluff.\n"
            "All growth is grassroots. The more individuals activate, the faster we scale.\n"
            "Kendu is a canvas for builders, artists, thinkers, and doers. A decentralized brand with unstoppable momentum."
        ),
        "faq_is_dog_token": (
            "🐕 <b>Is Kendu just another dog/animal token?</b>\n\n"
            "Nope. The logo represents loyalty and tenacity — but Kendu isn’t about animal memes.\n"
            "It’s a culture, not a gimmick.\n"
            "A social brand for creatives, entrepreneurs, and dreamers building something real."
        ),
        "faq_next_level": (
            "🚀 <b>What will take Kendu to the next level?</b>\n\n"
            "You. Your voice, your energy, your network.\n"
            "There’s no ceiling if every holder becomes a marketer, creator, or builder.\n"
            "This is the difference between a coin that pumps and a movement that endures."
        ),
        "faq_help": (
            "🙋 <b>How can I help?</b>\n\n"
            "1. Post on X, Reddit, TikTok, etc\n"
            "2. Make content or memes\n"
            "3. Comment, reply, amplify\n"
            "4. Tell people IRL\n"
            "5. Build something\n\n"
            "If you’ve got skills — use them. If not, show up daily. That’s all it takes."
        ),
        "faq_marketcap": (
            "📈 <b>When are we reaching ___ market cap?</b>\n\n"
            "When we earn it. Every viral moment, every new holder, every tweet compounds.\n"
            "We grow through consistent action, not hype cycles.\n"
            "10B isn’t a meme — it’s the result of community scaling and conviction."
        ),
        "faq_dipping": (
            "📉 <b>Why is Kendu dipping/pumping?</b>\n\n"
            "Markets breathe. Dips are redistribution.\n"
            "Strong hands stay focused, weak hands get shaken out.\n"
            "If you're zoomed out, you see consolidation — not panic.\n"
            "This is where conviction compounds. We don’t gamble. We work."
        ),
        "faq_safety": (
            "🛡️ <b>How can I keep my tokens safe?</b>\n\n"
            "• Never share your seed phrase — no matter what\n"
            "• Don’t click random links or connect unknown dApps\n"
            "• Use a hardware wallet for large holdings\n"
            "• Join Telegram from kendu.io — not search\n"
            "Security = responsibility. Protect your keys."
        )
    }

    if question_id not in answers:
        return

    text = answers[question_id]
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="faq")]
    ])

    msg_id = context.user_data.get("menu_msg_id")
    if msg_id:
        await edit_menu_response(context, update.effective_chat.id, msg_id, text, reply_markup)
