from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ui.menu_renderer import menu_renderer
from core.menu_state import should_skip_section_render
from core.price_fetcher import get_kendu_price_panel


# ===== Buy Kendu Menu =====
async def handle_buy_kendu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await should_skip_section_render(update, context, section_type="text", section_key="buy"):
        return

    print("🛒 Buy menu opened")

    base_text = (
        "💰 <b>Buy $KENDU</b>\n\n"
        "Kendu is available on <b>Ethereum</b>, <b>Solana</b>, and <b>Base</b>.\n"
        "Kendu is accessible to all. 🌍\n\n"
        "We primarily identify as an <b>Ethereum token</b>, but support access across major ecosystems.\n"
        "Liquidity pools are available on each chain for accessibility and growth.\n\n"
        "⚫ <b>Ethereum (ETH)</b>\n"
        "<code>0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18</code>\n\n"
        "🟣 <b>Solana (SOL)</b>\n"
        "<code>2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45</code>\n\n"
        "🔵 <b>Base (BASE)</b>\n"
        "<code>0xef73611F98DA6E57e0776317957af61B59E09Ed7</code>\n\n"
        "📌 <i>Use a trusted wallet & verify all contracts via /contracts</i>\n\n"
    )

    price_panel = await get_kendu_price_panel()
    full_text = f"{base_text}{price_panel}"

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚫ Buy on Ethereum (ETH)", callback_data="buy_eth")],
        [InlineKeyboardButton("🟣 Buy on Solana (SOL)", callback_data="buy_sol")],
        [InlineKeyboardButton("🔵 Buy on Base (BASE)", callback_data="buy_base")],
        [InlineKeyboardButton("🔄 Refresh Prices", callback_data="refresh_prices")],
        [InlineKeyboardButton("🔙 Back", callback_data="menu")]
    ])

    await menu_renderer(
        update=update,
        context=context,
        msg_type="text",
        text=full_text,
        reply_markup=reply_markup,
        section_key="buy"
    )


# ===== Buy on Individual Chains =====
async def handle_buy_chain(update: Update, context: ContextTypes.DEFAULT_TYPE, chain: str):
    print(f"🧾 Showing DEX instructions for: {chain.upper()}")

    chains = {
        "buy_eth": {
            "title": "⚫ <b>Buy on Ethereum (ETH)</b>",
            "why": [
                "Deepest liquidity 💧",
                "Largest number of long-term holders 🧠",
                "Best for conviction plays 💎",
                "Access to top dApps like Uniswap"
            ],
            "dex": "Uniswap",
            "link": "https://app.uniswap.org/swap?outputCurrency=0xaa95f26e30001251fb905d264aa7b00ee9df6c18&inputCurrency=ETH",
            "contract": "0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18"
        },
        "buy_sol": {
            "title": "🟣 <b>Buy on Solana (SOL)</b>",
            "why": [
                "Lightning fast ⚡",
                "Virtually no gas 🤑",
                "Great for high-frequency trading 🚀"
            ],
            "dex": "Raydium",
            "link": "https://raydium.io/swap/?inputMint=sol&outputMint=2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45",
            "contract": "2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45"
        },
        "buy_base": {
            "title": "🔵 <b>Buy on Base (BASE)</b>",
            "why": [
                "Fast transactions ⚡",
                "Low gas fees 🧾",
                "Powered by Coinbase 🏦"
            ],
            "dex": "Aerodrome",
            "link": "https://aerodrome.finance/swap?from=eth&to=0xef73611f98da6e57e0776317957af61b59e09ed7&chain0=8453&chain1=8453",
            "contract": "0xef73611F98DA6E57e0776317957af61B59E09Ed7"
        }
    }

    data = chains.get(chain)
    if not data:
        print("❌ Invalid chain passed to handle_buy_chain")
        return

    text = (
        f"{data['title']}\n\n"
        "<b>Why buy here?</b>\n" +
        "\n".join(f"• {reason}" for reason in data["why"]) +
        f"\n\n<b>Recommended DEX:</b> {data['dex']}\n\n"
        f"<b>Contract Address:</b>\n<code>{data['contract']}</code>\n\n"
        "⚠️ Always verify the contract before trading."
    )

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Trade Now", url=data["link"])],
        [InlineKeyboardButton("🔙 Back", callback_data="buy_kendu")]
    ])

    await menu_renderer(
        update=update,
        context=context,
        msg_type="text",
        text=text,
        reply_markup=reply_markup,
        section_key=chain
    )


# ===== Refresh Button Callback =====
async def handle_refresh_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("🔄 Refreshing price panel...")
    await handle_buy_kendu(update, context)
