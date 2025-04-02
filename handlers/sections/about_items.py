from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from ui.menu_renderer import menu_renderer


async def handle_about_item(update: Update, context: ContextTypes.DEFAULT_TYPE, item: str):
    """
    Displays an individual About section (text-only) using menu_renderer.
    """

    about_map = {
        "about_holders": {
            "title": "🔗 <b>Power to the Holders</b>",
            "desc": (
                "Kendu gives its holders the power to shape their future.\n"
                "It’s a social movement and a crypto brand umbrella that houses community-led businesses, products, and endeavours.\n"
                "We inspire a culture of <b>hard work</b>, <b>excellence</b>, and <b>accountability</b>.\n\n"
                "We believe in the power of both the individual and the collective.\n"
                "Unleash your potential and witness what you're truly capable of.\n"
                "<b>It’s all for one, and one for all.</b>\n"
                "We work around the clock, every day of the year."
            )
        },
        "about_builders": {
            "title": "🧱 <b>For the Builders</b>",
            "desc": (
                "Kendu attracts <b>builders</b>, <b>doers</b>, <b>go-getters</b>, <b>artists</b>, and <b>the good</b> — those who create, not wait.\n"
                "We invite you to dive into the next multi-billion dollar crypto giant: <b>Kendu.</b>"
            )
        },
        "about_irl": {
            "title": "🌍 <b>Bringing Crypto IRL</b>",
            "desc": (
                "Kendu sets out to do the impossible: build a purely organic crypto brand in a sea of cabal tokens, pump and dumps, insider trading, snipes, manufactured hype and FOMO.\n"
                "<b>Build with Kendu. Watch your ideas come to life.</b>\n"
                "We grow with long-term vision, brick by brick, one heart at a time."
            )
        },
        "about_community": {
            "title": "📣 <b>A Masterclass in Community Building</b>",
            "desc": (
                "Kendu is a truly organic movement with no paid engagement or fake activity.\n"
                "Holders are encouraged to step up in their own way, whether through <b>social posts, speaking on Spaces, building Kendu businesses, or repping Kendu IRL</b>.\n"
                "Tokens only reach super scale with full community activation.\n"
                "<b>Be loud, be unignorable, do what others won’t. The more who activate, the faster Kendu rises.</b>\n"
                "Who will you be in Kendu?"
            )
        },
        "about_kendumanchad": {
            "title": "🎥 <b>Kendu Man Saves DeFi</b>",
            "desc": (
                "In Q3 2024, Kendu held one of DeFi’s biggest giveaways—<b>1 billion $KENDU, worth around $50,000</b> at the time, for the most creative promo video.\n"
                "Over 20 entries came in, and OG member Trips won with his <b>“Kendu Man”</b> video.\n"
                "He also proudly sports one of the largest Kendu tattoos across his ribs."
            )
        }
    }

    item_data = about_map.get(item)

    if not item_data:
        print(f"❌ Unknown about item: {item}")
        await menu_renderer(
            update=update,
            context=context,
            msg_type="text",
            text="⚠️ This section is no longer available.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="about")]]),
            section_key="unknown_about"
        )
        return

    print(f"🧠 Showing about item: {item}")

    text = f"{item_data['title']}\n\n{item_data['desc']}"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="about")]
    ])

    await menu_renderer(
        update=update,
        context=context,
        msg_type="text",
        text=text,
        reply_markup=reply_markup,
        section_key=item
    )
