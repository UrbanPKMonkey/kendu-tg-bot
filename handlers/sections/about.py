# handlers/sections/about.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.menu_handler import menu_handler

async def handle_about(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message):
    # Check if we should skip rendering
    if await menu_handler(context, chat_id, message, current_type="text"):
        return

    text = (
        "🧠 <b>About Kendu</b>\n\n"
        "Kendu is a movement that empowers you to turn your life goals into reality.\n"
        "Take initiative, and the community will fuel your journey.\n"
        "<b>What is your dream? 💭</b>\n\n"
        "🔗 <b>Power to the Holders</b>\n"
        "Kendu gives its holders the power to shape their future.\n"
        "It’s a social movement and a crypto brand umbrella that houses community-led businesses, products, and endeavours.\n"
        "We inspire a culture of <b>hard work</b>, <b>excellence</b>, and <b>accountability</b> across our vibrant community.\n\n"
        "We believe in the power of both the individual and the collective.\n"
        "Unleash your potential and witness what you're truly capable of — compounding the already unstoppable innovation and tenacity of the Kendu community.\n"
        "<b>It’s all for one, and one for all.</b>\n"
        "We work around the clock, every day of the year.\n\n"
        "🧱 <b>For the Builders</b>\n"
        "Kendu attracts <b>builders</b>, <b>doers</b>, <b>go-getters</b>, <b>artists</b>, and <b>the good</b> — those who create, not wait.\n"
        "We invite you to dive into the next multi-billion dollar crypto giant: <b>Kendu.</b>\n\n"
        "🌍 <b>Bringing Crypto IRL</b>\n"
        "Kendu sets out to do the impossible: build a purely organic crypto brand in a sea of cabal tokens, pump and dumps, insider trading, snipes, manufactured hype and FOMO.\n"
        "The game has been rigged against you — until now.\n"
        "<b>Build with Kendu. Watch your ideas come to life.</b>\n"
        "We grow with long-term vision, brick by brick, one heart at a time.\n\n"
        "📣 <b>A Masterclass in Community Building</b>\n"
        "Kendu is a truly organic movement — no paid engagement, no fake activity.\n"
        "Holders are encouraged to step up in their own way:\n"
        "• Social posts\n"
        "• Speaking on Spaces\n"
        "• Building businesses\n"
        "• Repping Kendu IRL\n\n"
        "Tokens only reach super scale with full community activation.\n"
        "<b>The more who activate, the faster Kendu rises.</b>\n"
        "Who will you be in Kendu?\n\n"
        "🎥 <b>Kendu Man Saves DeFi</b>\n"
        "In Q3 2024, Kendu hosted one of DeFi’s biggest giveaways —\n"
        "<b>1 billion $KENDU (~$50,000)</b> for the most creative promo video.\n"
        "Over 20 entries came in.\n"
        "OG member <b>Trips</b> won with his “Kendu Man” video — and now proudly wears one of the largest Kendu tattoos across his ribs.\n\n"
        "🪖 <b>We don’t gamble. We work!</b>"
    )

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="menu")]
    ])

    sent = await context.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    context.user_data["menu_msg_id"] = sent.message_id
    context.user_data["menu_msg_type"] = "text"
