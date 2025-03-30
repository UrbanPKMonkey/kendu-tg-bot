from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
from utils.message_tools import smart_send_or_edit, add_black_background_to_image, get_contracts_text_and_markup

import logging
logger = logging.getLogger(__name__)


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

async def handle_button(update: Update = None, context: ContextTypes.DEFAULT_TYPE = None, data_override=None, message_override=None):
    query = update.callback_query if update else None
    data = query.data if query else data_override
    chat_id = (query.message.chat_id if query else message_override.chat_id)

    if query:
        await query.answer()

    if data == "menu":
        text = (
            "🤖 <b>Kendu Main Menu</b>\n\n"
            "Tap an option below to explore:"
        )

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🧠 About", callback_data="about")],
            [InlineKeyboardButton("🌐 Ecosystem", callback_data="ecosystem")],
            [InlineKeyboardButton("💰 Buy Kendu", callback_data="buy_kendu")],
            [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
            [InlineKeyboardButton("🧾 Contract Addresses", callback_data="contract_addresses")],
            [InlineKeyboardButton("🔗 Follow", callback_data="follow_links")]
        ])

        # 🧼 Always delete the previous message if it's a photo (like from /start)
        try:
            await query.message.delete()
        except Exception:
            pass  # Message already deleted or failed silently

        sent = await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

        # 💾 Save new menu message ID
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

        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="menu")]])

        await smart_send_or_edit(
            query=query,
            context=context,
            new_text=text,
            reply_markup=reply_markup,
            message_override=message_override
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
            reply_markup=reply_markup,
            message_override=message_override
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
        photo_url = await add_black_background_to_image("https://www.kendu.io/assets/images/kendu-style-logo.png")
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
            "💰 <b>Buy $KENDU</b>\n\n"
            "Kendu is available on <b>Ethereum</b>, <b>Solana</b>, and <b>Base</b>.\n"
            "Kendu is accessible to all. 🌍\n\n"

            "At Kendu, we primarily identify as an <b>Ethereum token</b>, but we believe in broad access to $KENDU across ecosystems.\n"
            "To support this, we’ve seeded additional liquidity pools on popular blockchains, allowing $KENDU to be bought and traded beyond Ethereum.\n"
            "There are a few easy ways to buy $KENDU. Whether you’re on Ethereum, Solana, Base, or just getting started, you’ll find simple steps below to get what you need and join the Kendu movement.\n\n"

            "⚫ <b>Ethereum (ETH)</b>\n"
            "<code>   0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18</code>\n"
            "   • Most active Kendu holders\n"
            "   • Highest liquidity\n"
            "   • Strongest long-term conviction\n\n"

            "🟣 <b>Solana (SOL)</b>\n"
            "<code>   2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45</code>\n"
            "   • Fast transactions\n"
            "   • Ultra-low gas fees\n"
            "   • Great for high-frequency trading\n\n"

            "🔵 <b>Base (BASE)</b>\n"
            "<code>   0xef73611F98DA6E57e0776317957af61B59E09Ed7</code>\n"
            "   • Low-cost memecoin ecosystem\n"
            "   • Bridges EVM familiarity with low fees\n"
            "   • Growing rapidly with community projects\n\n"

            "📌 <i>Tip:</i> Make sure you're using a trusted wallet (like Metamask or Phantom) and verify contract addresses directly from the official /contracts section."
        )

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚫ Buy on Ethereum (ETH)", callback_data="buy_eth")],
            [InlineKeyboardButton("🟣 Buy on Solana (SOL)", callback_data="buy_sol")],
            [InlineKeyboardButton("🔵 Buy on Base (BASE)", callback_data="buy_base")],
            [InlineKeyboardButton("🔁 How to Bridge", callback_data="how_to_bridge")],
            [InlineKeyboardButton("🔙 Back", callback_data="menu")]
        ])

        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, reply_markup)


    elif data == "buy_eth":
        text = (
            "⚫ <b>Buy on Ethereum (ETH)</b>\n\n"
            "Ethereum is Kendu’s home — and the primary chain for $KENDU.\n\n"

            "<b>Why buy on ETH?</b>\n"
            "• Deepest liquidity 💧\n"
            "• Largest number of long-term holders 🧠\n"
            "• Full access to core Ethereum dApps (e.g. Uniswap, Etherscan, etc.)\n"
            "• Best for long-term conviction plays 💎\n\n"

            "<b>Recommended DEX:</b> Uniswap\n\n"

            "<b>Contract Address:</b>\n"
            "<code>0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18</code>\n\n"
            "⚠️ Always verify the contract address before trading."
        )

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 Buy on Uniswap", url="https://app.uniswap.org/swap?outputCurrency=0xaa95f26e30001251fb905d264aa7b00ee9df6c18&inputCurrency=ETH")],
            [InlineKeyboardButton("❓ How to Buy on ETH", callback_data="how_to_buy_eth")],
            [InlineKeyboardButton("🔙 Back", callback_data="buy_kendu")]
        ])

        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, reply_markup)



    elif data == "buy_sol":
        text = (
            "🟣 <b>Buy on Solana (SOL)</b>\n\n"
            "Solana offers lightning-fast speeds and almost zero gas fees.\n\n"

            "<b>Why buy on SOL?</b>\n"
            "• Near-instant transactions ⚡\n"
            "• Virtually no gas fees 🤑\n"
            "• Ideal for trading smaller sizes or onboarding friends 👥\n"
            "• Great for degen speedruns and creators 🚀\n\n"
            "<b>Recommended DEX:</b> Raydium\n\n"

            "<b>Contract Address:</b>\n"
            "<code>2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45</code>\n\n"
            "⚠️ Always verify the contract address before trading."
        )

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 Buy on Raydium", url="https://raydium.io/swap/?inputMint=sol&outputMint=2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45")],
            [InlineKeyboardButton("❓ How to Buy on SOL", callback_data="how_to_buy_sol")],
            [InlineKeyboardButton("🔙 Back", callback_data="buy_kendu")]
        ])

        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, reply_markup)



    elif data == "buy_base":
        text = (
            "🔵 <b>Buy on Base (BASE)</b>\n\n"
            "Base is a fast-growing L2 backed by Coinbase.\n\n"

            "<b>Why buy on BASE?</b>\n"
            "• Fast transactions ⚡\n"
            "• Low fees compared to Ethereum 🧾\n"
            "• Easy onboarding via Coinbase 🏦\n"
            "• Base has one of the strongest meme communities 🔥\n\n"
            "<b>Recommended DEX:</b> Aerodrome\n\n"

            "<b>Contract Address:</b>\n"
            "<code>0xef73611F98DA6E57e0776317957af61B59E09Ed7</code>\n\n"
            "⚠️ Always verify the contract address before trading."
        )

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 Buy on Aerodrome", url="https://aerodrome.finance/swap?from=eth&to=0xef73611f98da6e57e0776317957af61b59e09ed7&chain0=8453&chain1=8453")],
            [InlineKeyboardButton("❓ How to Buy on BASE", callback_data="how_to_buy_base")],
            [InlineKeyboardButton("🔙 Back", callback_data="buy_kendu")]
        ])

        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, reply_markup)





    elif data == "faq":
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
            await edit_menu_response(context, chat_id, msg_id, text, reply_markup)


    elif data == "faq_what_is_kendu":
        text = (
            "🔸 <b>What is Kendu?</b>\n\n"
            "Kendu is a memecoin ecosystem and social movement led and driven forward by its community through organic effort. We don't engage in paid marketing or use bots and market makers to fake engagement, volume, or floor price; instead, we rely on the daily efforts of our autonomous community members to grow; the more profound the consistent activation of the individual, the higher Kendu will go. Each member's contributions are crucial to the project's success, creating an infinitely scalable approach that fosters infectious virality.\n"
            "This grassroots effort makes Kendu unique, with a community unparalleled in dedication, conviction, and working ethos. Kendu's success at scale is a matter of time and work, but the pace depends on our collective and individual efforts. While the ecosystem will support dApps and products, their impact hinges on the strength of the Kendu army, making community activation the perpetual focus.\n\n"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="faq")]])
        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, reply_markup)

    elif data == "faq_is_dog_token":
        text = (
            "🐕 <b>Is Kendu just another dog/animal token?</b>\n\n"
            "No, Kendu's original IP logo and name only represent the tenacity and loyalty of its community. They have nothing to do with narrative, memetic value, a flavour of the month TikTok animal trend, or anything of the sort.\n"
            "Once you join the community, you will quickly see Kendu as much more than such reductionist language.\n"
            "What is important to any token is not the narrative but rather the culture formed in its community. Kendu can be anything to you, to some it's art, to some it's a movement, to some it's a supportive network, and to many it is home.\n"
            "Kendu is your canvas to paint on, and you are free to form your own ideas on what it means to you.\n\n"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="faq")]])
        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, reply_markup)

    elif data == "faq_next_level":
        text = (
            "🚀 <b>What will take Kendu to the next level?</b>\n\n"
            "You are the key to Kendu's next level. No one on this planet has your unique network, skills, and talents, which make you an indispensable asset in the project's growth and scale. You can become far more powerful and influential than you imagine, not just in the value and holders you can bring to Kendu, but in life. With your unique capabilities, you have the power to drive Kendu forward in your own way; you need only try.\n\n"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="faq")]])
        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, reply_markup)

    elif data == "faq_help":
        text = (
            "🙋 <b>How can I help?</b>\n\n"
            "There are thousands of ways to help, but a good start is by creating social media accounts on platforms like Reddit, X, TikTok, and YouTube, if you haven't already. Engage with community posts by replying, liking, sharing, and increasing engagement thoughtfully—avoid one-word comments like LFG!. Create your own posts to spread the word about Kendu. Tell people in your life, put up posters in your town, make stickers, create content. Get crazy! Please remember to always be kind and respectful when discussing Kendu online, as you represent the project. Avoid negative talk about other projects and refrain from engaging with those who try to provoke the community.\n\n"
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="faq")]])
        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, reply_markup)

    elif data == "faq_marketcap":
        text = (
            "📈 <b>When are we reaching ___ market cap?</b>\n\n"
            "We can't predict the exact timing, but we know that the Kendu community's daily efforts—spreading the word on social media and in real-life—drive growth. Think of crypto as a giant numbers game; despite short and medium-term volatility, when you become the loudest in the room and onboard the most people, the marketcap will eventually reflect that. When you activate and inspire others to do the same, you can single-handedly create a snowball effect. Since Kendu is original IP and not tied to any fleeting narrative or temporary hype cycle, Kendu's approach to project growth is infinitely scalable and has no ceiling. When the community says, $10B is programmed, they mean that we can reach limitless heights with consistent, organic marketing at scale.\n\n"

        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="faq")]])
        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, reply_markup)

    elif data == "faq_dipping":
        text = (
            "📉 <b>Why is Kendu dipping/pumping?</b>\n\n"
            "Crypto is a volatile market, and memecoins even more so. You must be emotionally prepared for volatility to experience the enormous upside on the other side. Markets naturally fluctuate, similar to how humans breathe. After a sharp rise (a big breath in), people may take profits, leading to price corrections (breathing out); this process is called redistribution. It allows new members to enter at lower prices, redistributing tokens from large inactive early holders to new, active community members. Looking back on the charts of top successful projects, including Bitcoin, you'll notice multiple periods of redistribution and consolidation following parabolic moves to the upside. Each time a token/coin goes through this and comes out on the other side, it strengthens.\n"
            "It's essential to zoom out and focus on the bigger picture during volatile periods. You're likely witnessing market consolidation, which is a healthy phase following significant price increases. During consolidation, a token finds its new price floor before rising to new heights in a price discovery phase. Trust in yourself and the community and continue contributing to the daily work. We can't control market forces or individual actions, but we can control our collective efforts and personal initiatives.\n"
            "Regardless of market conditions, we work tirelessly and happily towards Kendu's goal of becoming a household name in crypto. We are focused on long-term growth and remain unaffected by short-term market movements.\n\n"

        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="faq")]])
        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, reply_markup)

    elif data == "faq_safety":
        text = (
            "🛡️ <b>How can I keep my tokens safe?</b>\n\n"
            "It's crucial to understand that your Kendu tokens are stored on the blockchain, not within your wallet app. Wallet apps simply hold the keys that allow you to access your tokens. This underscores the importance of choosing a wallet app that you trust, as you do not need to move your tokens between different apps.\n"
            "To keep your tokens safe, it's vital to never enter your seed phrase anywhere and store it securely offline, never digitally. Be extremely cautious about direct messages (DMs) and always verify the identity of anyone you're communicating with in public forums, to be extra safe, you should . Remember, there are no Kendu airdrops or similar giveaways; you will never be asked to connect your wallet to any external services or sites. Scammers use various tactics to steal tokens, so always exercise caution.\n"
            "If you have any doubts or questions, rest assured that help is readily available in the official Telegram group, which can be accessed via the links on this site.\n\n"
          
        )
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="faq")]])
        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, reply_markup)


    elif data == "contract_addresses":
        text, reply_markup = get_contracts_text_and_markup()
        await smart_send_or_edit(
            query=query,
            context=context,
            new_text=text,
            reply_markup=reply_markup,
            message_override=message_override
        )

    elif data == "follow_links":
        text = "🔗 <b>Follow Kendu</b>\n\nExplore our ecosystem and stay connected 👇"

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🌐 Official Website", url="https://kendu.io")],
            [InlineKeyboardButton("💬 Telegram", url="https://t.me/Kendu")],
            [InlineKeyboardButton("📣 Twitter/X", url="https://x.com/KenduInu")],
            [InlineKeyboardButton("📰 Reddit", url="https://www.reddit.com/r/KenduInu_Ecosystem")],
            [InlineKeyboardButton("🔧 Dextools", url="https://www.dextools.io/app/en/ether/pair-explorer/0xd9f2a7471d1998c69de5cae6df5d3f070f01df9f?t=1708519310322")],
            [InlineKeyboardButton("🎥 YouTube", url="https://www.youtube.com/@KenduInuArmy")],
            [InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/kenduinuofficial")],
            [InlineKeyboardButton("💹 Stocktwits", url="https://stocktwits.com/KenduCTO")],
            [InlineKeyboardButton("⚫ Etherscan (ETH)", url="https://etherscan.io/token/0xaa95f26e30001251fb905d264aa7b00ee9df6c18")],
            [InlineKeyboardButton("🟣 Solscan (SOL)", url="https://solscan.io/token/2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45")],
            [InlineKeyboardButton("🔵 Basescan (BASE)", url="https://basescan.org/token/0xef73611f98da6e57e0776317957af61b59e09ed7")],
            [InlineKeyboardButton("💰 CoinMarketCap", url="https://coinmarketcap.com/currencies/kendu-inu/")],
            [InlineKeyboardButton("🔙 Back", callback_data="menu")]
        ])
        await smart_send_or_edit(
            query=query,
            context=context,
            new_text=text,
            reply_markup=reply_markup,
            message_override=message_override
        )

    else:
        text = "⚠️ Unknown command. Please use /menu to get back to the main screen."
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🤖 Back to Menu", callback_data="menu")]
        ])
        await smart_send_or_edit(
            query=query,
            context=context,
            new_text=text,
            reply_markup=reply_markup,
            message_override=message_override
        )

