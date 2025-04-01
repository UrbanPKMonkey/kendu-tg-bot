# handlers/sections/ecosystem_items.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.message_tools import add_black_background_to_image
from utils.menu_handler import menu_handler

async def handle_ecosystem_item(context: ContextTypes.DEFAULT_TYPE, chat_id: int, item: str):
    ecosystem_map = {
        "kendu_energy": {
            "title": "⚡ <b>Kendu Energy Drink</b>",
            "desc": "Fuel your grind with Kendu Energy — the first community-powered energy drink built for creators, coders, traders, and builders.\nAll flavor. No compromise. One sip to become a chad.",
            "photo": "https://www.kendu.io/assets/images/kendu-energy-drink.webp",
            "url": "https://kenduenergy.com/products/energy-drinks-usa-can-aus"
        },
        "kendu_coffee": {
            "title": "☕ <b>Kendu Coffee</b>",
            "desc": "Bold, organic, and unstoppable — Kendu Coffee fuels builders the way nature intended.\nWake up with purpose and taste the difference of decentralized hustle.",
            "photo": "https://www.kendu.io/assets/images/kendu-coffee.webp",
            "url": "https://kenducoffee.com/"
        },
        "kendu_creator": {
            "title": "🎨 <b>Kendu Creator</b>",
            "desc": "A space for artists, devs, designers, and thinkers to create, collab, and build for the culture.\nShowcase your talent, contribute your skills, and be part of something legendary.",
            "photo": "https://www.kendu.io/assets/images/kenducreator.png",
            "url": "https://kenducreator.com/"
        },
        "kendu_style": {
            "title": "🧢 <b>Kendu Style</b>",
            "desc": "Rep the movement IRL. Kendu Style is bold, raw, and unmistakably you.\nCaps, tees, fits — made for the builders, doers, and believers.",
            "photo": await add_black_background_to_image("https://www.kendu.io/assets/images/kendu-style-logo.png"),
            "url": "https://kendustyle.com/"
        },
        "kendu_unstitched": {
            "title": "🧵 <b>Kendu Unstitched</b>",
            "desc": "Where crypto meets culture. A raw fashion expression of the Kendu spirit.\nUnbranded. Unfiltered. Unstoppable.",
            "photo": "https://www.kendu.io/assets/images/kendustiched.webp",
            "url": "https://kendu-unstitched.square.site/"
        }
    }

    item_data = ecosystem_map.get(item)
    if not item_data:
        return

    # Prevent duplicate loads
    if await menu_handler(context, chat_id, None, current_type="photo"):
        return

    # Delete old tracked message if not already deleted
    old_msg_id = context.user_data.get("menu_msg_id")
    try:
        if old_msg_id:
            await context.bot.delete_message(chat_id=chat_id, message_id=old_msg_id)
    except Exception:
        pass

    # Build photo content
    caption = f"{item_data['title']}\n\n{item_data['desc']}"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Visit Site", url=item_data['url'])],
        [InlineKeyboardButton("🔙 Back", callback_data="ecosystem")]
    ])

    sent = await context.bot.send_photo(
        chat_id=chat_id,
        photo=item_data["photo"],
        caption=caption,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

    context.user_data["menu_msg_id"] = sent.message_id
    context.user_data["menu_msg_type"] = "photo"
