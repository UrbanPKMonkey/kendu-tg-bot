from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.menu_state import should_skip_section_render
from ui.menu_renderer import menu_renderer

# ===== 🤔 FAQ Menu =====
async def handle_faq_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await should_skip_section_render(update, context, section_type="text", section_key="faq"):
        return

    print("📚 Showing FAQ menu")

    text = (
        "❓ <b>Frequently Asked Questions</b>\n\n"
        "Welcome to the Kendu FAQ — no fluff, no filters, just real answers.\n"
        "Whether you're new to the movement or a seasoned builder, these are the most common questions from the community.\n"
        "We don’t sugarcoat. We don’t do smoke and mirrors.\n"
        "If you're here, you're ready to do the work.\n\n"
        "👇 Tap a question to learn more."
        )

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🧠 What is Kendu?", callback_data="faq_what_is_kendu")],
        [InlineKeyboardButton("🐕 Is Kendu just another dog token?", callback_data="faq_is_dog_token")],
        [InlineKeyboardButton("🚀 What will take Kendu to the next level?", callback_data="faq_next_level")],
        [InlineKeyboardButton("🙋 How can I help?", callback_data="faq_help")],
        [InlineKeyboardButton("📈 When are we reaching ___ market cap?", callback_data="faq_marketcap")],
        [InlineKeyboardButton("📉 Why is Kendu dipping/pumping?", callback_data="faq_dipping")],
        [InlineKeyboardButton("🔒 How can I keep my tokens safe?", callback_data="faq_safety")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu")]
    ])

    await menu_renderer(
        update=update,
        context=context,
        msg_type="text",
        text=text,
        reply_markup=reply_markup,
        section_key="faq"
    )

# ===== 📖 Answer Specific FAQ =====
async def handle_faq_answer(update: Update, context: ContextTypes.DEFAULT_TYPE, data: str):
    print(f"📖 Showing FAQ answer for: {data}")

    faq_data = {
        "faq_what_is_kendu": (
            "🧠 <b>What is Kendu?</b>\n\n"
            "Kendu is a memecoin ecosystem and social movement led and driven forward by its community through organic effort. We don't engage in paid marketing or use bots and market makers to fake engagement, volume, or floor price; instead, we rely on the daily efforts of our autonomous community members to grow; the more profound the consistent activation of the individual, the higher Kendu will go. Each member's contributions are crucial to the project's success, creating an infinitely scalable approach that fosters infectious virality.\n\n"
            "This grassroots effort makes Kendu unique, with a community unparalleled in dedication, conviction, and working ethos. Kendu's success at scale is a matter of time and work, but the pace depends on our collective and individual efforts. While the ecosystem will support dApps and products, their impact hinges on the strength of the Kendu army, making community activation the perpetual focus."

        ),
        "faq_is_dog_token": (
            "🐕 <b>Is Kendu just another dog/animal token?</b>\n\n"
            "No, Kendu's original IP logo and name only represent the tenacity and loyalty of its community. They have nothing to do with narrative, memetic value, a flavour of the month TikTok animal trend, or anything of the sort.\n\n"
            "Once you join the community, you will quickly see Kendu as much more than such reductionist language.\n\n"
            "What is important to any token is not the narrative but rather the culture formed in its community. Kendu can be anything to you, to some it's art, to some it's a movement, to some it's a supportive network, and to many it is home.\n\n"
            "Kendu is your canvas to paint on, and you are free to form your own ideas on what it means to you."
        ),
        "faq_next_level": (
            "🚀 <b>What will take Kendu to the next level?</b>\n\n"
            "You are the key to Kendu's next level. No one on this planet has your unique network, skills, and talents, which make you an indispensable asset in the project's growth and scale. You can become far more powerful and influential than you imagine, not just in the value and holders you can bring to Kendu, but in life. With your unique capabilities, you have the power to drive Kendu forward in your own way; you need only try."
            
        ),
        "faq_help": (
            "🙋 <b>How can I help?</b>\n\n"
            "There are thousands of ways to help, but a good start is by creating social media accounts on platforms like Reddit, X, TikTok, and YouTube, if you haven't already. Engage with community posts by replying, liking, sharing, and increasing engagement thoughtfully—avoid one-word comments like LFG!. Create your own posts to spread the word about Kendu. Tell people in your life, put up posters in your town, make stickers, create content. Get crazy! Please remember to always be kind and respectful when discussing Kendu online, as you represent the project. Avoid negative talk about other projects and refrain from engaging with those who try to provoke the community."
           
        ),
        "faq_marketcap": (
            "📈 <b>When are we reaching ___ market cap?</b>\n\n"
            "We can't predict the exact timing, but we know that the Kendu community's daily efforts—spreading the word on social media and in real-life—drive growth. Think of crypto as a giant numbers game; despite short and medium-term volatility, when you become the loudest in the room and onboard the most people, the marketcap will eventually reflect that. When you activate and inspire others to do the same, you can single-handedly create a snowball effect. Since Kendu is original IP and not tied to any fleeting narrative or temporary hype cycle, Kendu's approach to project growth is infinitely scalable and has no ceiling. When the community says, $10B is programmed, they mean that we can reach limitless heights with consistent, organic marketing at scale."
            
        ),
        "faq_dipping": (
            "📉 <b>Why is Kendu dipping/pumping?</b>\n\n"
            "Crypto is a volatile market, and memecoins even more so. You must be emotionally prepared for volatility to experience the enormous upside on the other side. Markets naturally fluctuate, similar to how humans breathe. After a sharp rise (a big breath in), people may take profits, leading to price corrections (breathing out); this process is called redistribution. It allows new members to enter at lower prices, redistributing tokens from large inactive early holders to new, active community members. Looking back on the charts of top successful projects, including Bitcoin, you'll notice multiple periods of redistribution and consolidation following parabolic moves to the upside. Each time a token/coin goes through this and comes out on the other side, it strengthens.\n\n"
            "It's essential to zoom out and focus on the bigger picture during volatile periods. You're likely witnessing market consolidation, which is a healthy phase following significant price increases. During consolidation, a token finds its new price floor before rising to new heights in a price discovery phase. Trust in yourself and the community and continue contributing to the daily work. We can't control market forces or individual actions, but we can control our collective efforts and personal initiatives.\n\n"
            "Regardless of market conditions, we work tirelessly and happily towards Kendu's goal of becoming a household name in crypto. We are focused on long-term growth and remain unaffected by short-term market movements."
        ),
        "faq_safety": (
            "🔒 <b>How can I keep my tokens safe?</b>\n\n"
            "It's crucial to understand that your Kendu tokens are stored on the blockchain, not within your wallet app. Wallet apps simply hold the keys that allow you to access your tokens. This underscores the importance of choosing a wallet app that you trust, as you do not need to move your tokens between different apps.\n\n"
            "To keep your tokens safe, it's vital to never enter your seed phrase anywhere and store it securely offline, never digitally. Be extremely cautious about direct messages (DMs) and always verify the identity of anyone you're communicating with in public forums, to be extra safe, you should . Remember, there are no Kendu airdrops or similar giveaways; you will never be asked to connect your wallet to any external services or sites. Scammers use various tactics to steal tokens, so always exercise caution.\n\n"
            "If you have any doubts or questions, rest assured that help is readily available in the official Telegram group, which can be accessed via the links on this site."

        )
    }

    if data not in faq_data:
        print(f"⚠️ Unknown FAQ key: {data}")
        return

    text = faq_data[data]
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back", callback_data="faq")]
    ])

    await menu_renderer(
        update=update,
        context=context,
        msg_type="text",
        text=text,
        reply_markup=reply_markup,
        section_key=data
    )
