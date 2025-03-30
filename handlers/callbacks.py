from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from utils.message_tools import smart_send_or_edit

# Helper to build back button
back_button = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 Back", callback_data="menu")]]
)

# Helper function to send/edit the dedicated menu message
async def edit_menu_response(context, chat_id, message_id, text, reply_markup):
    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    await query.answer()
    chat_id = query.message.chat_id

    if data == "menu":
        keyboard = [
            [InlineKeyboardButton("🧠 About", callback_data="about")],
            [InlineKeyboardButton("🌐 Ecosystem", callback_data="ecosystem")],
            [InlineKeyboardButton("💰 Buy Kendu", callback_data="buy_kendu")],
            [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
            [InlineKeyboardButton("🧾 Contract Addresses", callback_data="contract_addresses")],
            [InlineKeyboardButton("🔗 Follow", callback_data="follow_links")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        msg_id = context.user_data.get("menu_msg_id")

        if msg_id:
            await context.bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=msg_id,
                text="🤖 <b>Kendu Main Menu</b>\n\nTap an option below to explore:",
                parse_mode="HTML",
                reply_markup=reply_markup
            )
        else:
            sent = await query.message.reply_text(
                "🤖 <b>Kendu Main Menu</b>\n\nTap an option below to explore:",
                parse_mode="HTML",
                reply_markup=reply_markup
            )
            context.user_data["menu_msg_id"] = sent.message_id

    elif data == "about":
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

        await smart_send_or_edit(
            query=query,
            context=context,
            new_text=text,
            reply_markup=back_button
        )


    elif data == "ecosystem":
        text = (
            "🌐 <b>Kendu Ecosystem</b>\n\n"
            "Kendu is more than a token —\n"
            "It’s a <b>permissionless, decentralized brand</b> with no limits on what can be built.\n\n"
            "The community has already turned belief into:\n"
            "• Real products\n"
            "• Community businesses\n"
            "• Viral content\n\n"
            "<b>Kendu is your launchpad</b> for whatever comes next.\n"
            "If you can dream it, you can build it. 💥\n\n"
            "Explore our Ecosystem 👇"
        )

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡ Kendu Energy Drink", callback_data="kendu_energy")],
            [InlineKeyboardButton("☕ Kendu Coffee", callback_data="kendu_coffee")],
            [InlineKeyboardButton("🎨 Kendu Creator", callback_data="kendu_creator")],
            [InlineKeyboardButton("🧢 Kendu Style", callback_data="kendu_style")],
            [InlineKeyboardButton("🧵 Kendu Unstitched", callback_data="kendu_unstitched")],
            [InlineKeyboardButton("🔙 Back", callback_data="menu")]
        ])

        await smart_send_or_edit(
            query=query,
            context=context,
            new_text=text,
            reply_markup=reply_markup
        )


    elif data == "kendu_energy":
        photo_url = "https://www.kendu.io/assets/images/kendu-energy-drink.webp"
        caption = (
            "⚡ <b>Kendu Energy Drink</b>\n\n"
            "Fuel your grind with Kendu Energy — the first community-powered energy drink built for creators, coders, traders, and builders.\n"
            "All flavor. No compromise. One sip to become a chad."
        )
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Visit Site", url="https://kenduenergy.com/products/energy-drinks-usa-can-aus")],
            [InlineKeyboardButton("🔙 Back", callback_data="ecosystem")]
        ])

        # Delete previous message and send image
        await query.message.delete()
        new_msg = await query.message.chat.send_photo(
            photo=photo_url,
            caption=caption,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

        # Track the new message ID so back works!
        context.user_data["menu_msg_id"] = new_msg.message_id


    elif data == "kendu_coffee":
        photo_url = "https://www.kendu.io/assets/images/kendu-coffee.webp"
        caption = (
            "☕ <b>Kendu Coffee</b>\n\n"
            "Bold, organic, and unstoppable — Kendu Coffee fuels builders the way nature intended.\n"
            "Wake up with purpose and taste the difference of decentralized hustle."
        )
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Visit Site", url="https://kenducoffee.com/")],
            [InlineKeyboardButton("🔙 Back", callback_data="ecosystem")]
        ])

        # Delete previous message and send image
        await query.message.delete()
        new_msg = await query.message.chat.send_photo(
            photo=photo_url,
            caption=caption,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

        # Track the new message ID so back works!
        context.user_data["menu_msg_id"] = new_msg.message_id


    elif data == "kendu_creator":
        photo_url = "https://www.kendu.io/assets/images/kenducreator.png"
        caption = (
            "🎨 <b>Kendu Creator</b>\n\n"
            "A space for artists, devs, designers, and thinkers to create, collab, and build for the culture.\n"
            "Showcase your talent, contribute your skills, and be part of something legendary."
        )
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Visit Site", url="https://kenducreator.com/")],
            [InlineKeyboardButton("🔙 Back", callback_data="ecosystem")]
        ])

        # Delete previous message and send image
        await query.message.delete()
        new_msg = await query.message.chat.send_photo(
            photo=photo_url,
            caption=caption,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

        # Track the new message ID so back works!
        context.user_data["menu_msg_id"] = new_msg.message_id      



    elif data == "kendu_style":
        photo_url = "https://www.kendu.io/assets/images/kendu-style-logo.png"
        caption = (
            "🧢 <b>Kendu Style</b>\n\n"
            "Rep the movement IRL. Kendu Style is bold, raw, and unmistakably you.\n"
            "Caps, tees, fits — made for the builders, doers, and believers."
        )
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Visit Site", url="https://kendustyle.com/")],
            [InlineKeyboardButton("🔙 Back", callback_data="ecosystem")]
        ])

        # Delete previous message and send image
        await query.message.delete()
        new_msg = await query.message.chat.send_photo(
            photo=photo_url,
            caption=caption,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

        # Track the new message ID so back works!
        context.user_data["menu_msg_id"] = new_msg.message_id



    elif data == "kendu_unstitched":
        photo_url = "https://www.kendu.io/assets/images/kendustiched.webp"
        caption = (
            "🧵 <b>Kendu Unstitched</b>\n\n"
            "Where crypto meets culture. A raw fashion expression of the Kendu spirit.\n"
            "Unbranded. Unfiltered. Unstoppable."
        )
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Visit Site", url="https://kendu-unstitched.square.site/")],
            [InlineKeyboardButton("🔙 Back", callback_data="ecosystem")]
        ])

        # Delete previous message and send image
        await query.message.delete()
        new_msg = await query.message.chat.send_photo(
            photo=photo_url,
            caption=caption,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

        # Track the new message ID so back works!
        context.user_data["menu_msg_id"] = new_msg.message_id

  

    elif data == "buy_kendu":
        text = (
            "💰 <b>How to Buy $KENDU</b>\n\n"
            "Kendu is available on <b>Ethereum</b>, <b>Solana</b>, and <b>Base</b>.\n"
            "Kendu is accessible to all. 🌍\n\n"

            "At Kendu, we primarily identify as an <b>Ethereum token</b>, but we believe in broad access to $KENDU across ecosystems.\n"
            "To support this, we’ve seeded additional liquidity pools on popular blockchains, allowing $KENDU to be bought and traded beyond Ethereum.\n\n"

            "⚫ <b>Ethereum (ETH)</b>\n"
            "🟣 <b>Solana (SOL)</b>\n"
            "🔵 <b>Base (BASE)</b>\n\n"

            "📌 <b>Recommended Tool:</b> @coinrankerbot\n"
            "Buy directly from Telegram with speed & safety.\n\n"

            "🛒 <b>Trade Links:</b>\n"
            "⚫ <a href='https://www.dexscreener.com/ethereum/0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18'>Dexscreener (ETH)</a>\n"
            "🟣 <a href='https://www.dexscreener.com/solana/2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45'>Dexscreener (SOL)</a>\n"
            "🔵 <a href='https://www.dexscreener.com/base/0xef73611F98DA6E57e0776317957af61B59E09Ed7'>Dexscreener (BASE)</a>\n\n"

            "🧠 <i>Always verify contract addresses at /contracts before trading.</i>\n"
            "⚠️ <i>Kendu will never DM you. Never share your seed phrase.</i>"
        )

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 How to Buy", callback_data="how_to_buy")],
            [InlineKeyboardButton("🌉 How to Bridge", callback_data="how_to_bridge")],
            [InlineKeyboardButton("🔙 Back", callback_data="menu")]
        ])

        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, reply_markup)



    elif data == "faq":
        text = (
            "❓ <b>Frequently Asked Questions</b>\n\n"

            "🔸 <b>What is Kendu?</b>\n"
            "Kendu is a memecoin ecosystem and social movement led by a community of builders.\n"
            "We grow through organic action — no paid marketing, bots, or faked stats. Every individual matters.\n"
            "Our scale is infinite because our community activation is limitless.\n\n"

            "🔸 <b>Is Kendu just another dog/animal token?</b>\n"
            "Not at all. Kendu is original IP — it’s not driven by narrative fads or animal trends.\n"
            "It’s a canvas for expression and community building, and what you make of it is up to you.\n\n"

            "🔸 <b>What will take Kendu to the next level?</b>\n"
            "You. Your network, ideas, and conviction are the catalysts. This is grassroots crypto at its finest.\n\n"

            "🔸 <b>How can I help?</b>\n"
            "Start posting, replying, creating content, building IRL, and spreading the word.\n"
            "Be thoughtful. Be bold. Be respectful.\n\n"

            "🔸 <b>When are we reaching ___ market cap?</b>\n"
            "There’s no fixed path — just daily effort. $10B is programmed because we activate.\n"
            "When the noise and numbers compound, Kendu breaks through.\n\n"

            "🔸 <b>Why is Kendu dipping/pumping?</b>\n"
            "Volatility is normal. Every rise needs a breather. What matters is the community's strength during consolidation.\n"
            "Zoom out. Stay building. We’re here for the long game.\n\n"

            "🔸 <b>How can I keep my tokens safe?</b>\n"
            "Never share your seed phrase. Use a secure wallet. Ignore fake DMs, airdrops, and connect requests.\n"
            "When in doubt, ask the official Telegram: @Kendu\n\n"

            "🧠 <i>Stay alert, stay focused, and keep building.</i>"
        )

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="menu")]
        ])

        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, reply_markup)





    elif data == "contract_addresses":
        text = (
            "🧾 <b>Contract Addresses</b>\n\n"
            "ETH: 0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18\n"
            "SOL: 2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45\n"
            "BASE: 0xef73611F98DA6E57e0776317957af61B59E09Ed7"
        )
        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, back_button)

    elif data == "follow_links":
        text = (
            "🔗 <b>Social Links</b>\n\n"
            "🌐 <a href='https://kendu.io'>kendu.io</a>\n"
            "💬 <a href='https://t.me/Kendu'>Telegram</a>\n"
            "📣 <a href='https://x.com/KenduInu'>Twitter/X</a>\n"
            "📰 <a href='https://www.reddit.com/r/KenduInu_Ecosystem'>Reddit</a>"
        )
        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, back_button)
