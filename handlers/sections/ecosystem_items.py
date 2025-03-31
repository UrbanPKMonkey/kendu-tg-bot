# handlers/sections/ecosystem_items.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.message_tools import add_black_background_to_image

async def handle_ecosystem_item(context, chat_id, data):
    ecosystem_map = {
        "kendu_energy": {
            "photo": "https://www.kendu.io/assets/images/kendu-energy-drink.webp",
            "caption": (
                "⚡ <b>Kendu Energy Drink</b>\n\n"
                "Fuel your grind with Kendu Energy — the first community-powered energy drink built for creators, coders, traders, and builders.\n"
                "All flavor. No compromise. One sip to become a chad."
            ),
            "url": "https://kenduenergy.com/products/energy-drinks-usa-can-aus"
        },
        "kendu_coffee": {
            "photo": "https://www.kendu.io/assets/images/kendu-coffee.webp",
            "caption": (
                "☕ <b>Kendu Coffee</b>\n\n"
                "Bold, organic, and unstoppable — Kendu Coffee fuels builders the way nature intended.\n"
                "Wake up with purpose and taste the difference of decentralized hustle."
            ),
            "url": "https://kenducoffee.com/"
        },
        "kendu_creator": {
            "photo": "https://www.kendu.io/assets/images/kenducreator.png",
            "caption": (
                "🎨 <b>Kendu Creator</b>\n\n"
                "A space for artists, devs, designers, and thinkers to create, collab, and build for the culture.\n"
                "Showcase your talent, contribute your skills, and be part of something legendary."
            ),
            "url": "https://kenducreator.com/"
        },
        "kendu_style": {
            "photo": await add_black_background_to_image("https://www.kendu.io/assets/images/kendu-style-logo.png"),
            "caption": (
                "🧢 <b>Kendu Style</b>\n\n"
                "Rep the movement IRL. Kendu Style is bold, raw, and unmistakably you.\n"
                "Caps, tees, fits — made for the builders, doers, and believers."
            ),
            "url": "https://kendustyle.com/"
        },
        "kendu_unstitched": {
            "photo": "https://www.kendu.io/assets/images/kendustiched.webp",
            "caption": (
                "🧵 <b>Kendu Unstitched</b>\n\n"
                "Where crypto meets culture. A raw fashion expression of the Kendu spirit.\n"
                "Unbranded. Unfiltered. Unstoppable."
            ),
            "url": "https://kendu-unstitched.square.site/"
        }
    }

    item = ecosystem_map.get(data)
    if not item:
        return

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Visit Site", url=item["url"])],
        [InlineKeyboardButton("🔙 Back", callback_data="ecosystem")]
    ])

    # Delete previous message
    old_msg_id = context.user_data.get("menu_msg_id")
    try:
        if old_msg_id:
            await context.bot.delete_message(chat_id=chat_id, message_id=old_msg_id)
    except Exception:
        pass

    # Send image post
    sent = await context.bot.send_photo(
        chat_id=chat_id,
        photo=item["photo"],
        caption=item["caption"],
        parse_mode="HTML",
        reply_markup=reply_markup
    )

    context.user_data["menu_msg_id"] = sent.message_id
    context.user_data["menu_msg_type"] = "photo"
