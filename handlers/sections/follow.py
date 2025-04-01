# handlers/sections/follow.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.menu_handler import menu_handler
from utils.message_tools import smart_send_or_edit


async def handle_follow_links(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    update: Update = None,
):
    # Skip if already showing
    if await menu_handler(context, chat_id, update, current_type="text"):
        return

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
        context=context,
        query=update.callback_query if update else None,
        new_text=text,
        reply_markup=reply_markup,
        message_override=update.message if update else None,
    )

    context.user_data["menu_msg_type"] = "text"
