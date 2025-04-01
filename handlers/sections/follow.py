from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.menu_handler import menu_handler


async def handle_follow_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays Kendu's official social links and ecosystem connections."""
    print("🔗 Showing Kendu follow links")

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

    # Send the follow links menu
    await menu_handler(
        update=update,
        context=context,
        msg_type="text",
        text=text,
        reply_markup=reply_markup
    )
