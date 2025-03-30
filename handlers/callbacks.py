from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

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
            # ✅ Menu already exists — just update it
            await context.bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=msg_id,
                text="🤖 <b>Kendu Main Menu</b>\n\nTap an option below to explore:",
                parse_mode="HTML",
                reply_markup=reply_markup
            )
        else:
            # 🆕 First time: send the menu and store its ID
            sent = await query.message.reply_text(
                "🤖 <b>Kendu Main Menu</b>\n\nTap an option below to explore:",
                parse_mode="HTML",
                reply_markup=reply_markup
            )
            context.user_data["menu_msg_id"] = sent.message_id

    elif data == "about":
        text = text = (
            "🧠 <b>About Kendu</b>\n\n"
            "Kendu is a movement that empowers you to turn your life goals into reality.\n"
            "Take initiative, and the community will fuel your journey.\n"
            "<b>What is your dream? 💭</b>\n"

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
        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, back_button)

    elif data == "ecosystem":
        text = "🌐 <b>Kendu Ecosystem</b>\n\nThe Kendu ecosystem includes tools, community apps, and real-world products."
        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, back_button)

    elif data == "buy_kendu":
        text = "💰 <b>How to Buy Kendu</b>\n\nKendu is available on Ethereum, Solana, and Base.\n\nVisit /buykendu to learn more."
        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, back_button)

    elif data == "faq":
        text = "❓ <b>FAQ</b>\n\nAnswers to common questions are available at /faq"
        msg_id = context.user_data.get("menu_msg_id")
        if msg_id:
            await edit_menu_response(context, chat_id, msg_id, text, back_button)

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
