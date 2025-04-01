from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ui.menu_renderer import menu_renderer
from ui.menu_ui import add_black_background_to_image

async def handle_ecosystem_item(update: Update, context: ContextTypes.DEFAULT_TYPE, item: str):
    """
    Displays an individual ecosystem product page with image, description, and visit link.
    """

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
            "photo_fn": lambda: add_black_background_to_image("https://www.kendu.io/assets/images/kendu-style-logo.png"),
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
        print(f"❌ Unknown ecosystem item: {item}")
        await menu_renderer(
            update=update,
            context=context,
            msg_type="text",
            text="⚠️ This item is no longer available.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="ecosystem")]
            ])
        )
        return

    print(f"🌐 Showing ecosystem item: {item}")

    # Handle image dynamically for style with black background
    if "photo_fn" in item_data:
        photo = await item_data["photo_fn"]()
    else:
        photo = item_data["photo"]

    caption = f"{item_data['title']}\n\n{item_data['desc']}"
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Visit Site", url=item_data["url"])],
        [InlineKeyboardButton("🔙 Back", callback_data="ecosystem")]
    ])

    await menu_renderer(
        update=update,
        context=context,
        msg_type="text",
        text="⚠️ This item is no longer available.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="ecosystem")]
        ]),
        section_key="unknown_item"
    )
