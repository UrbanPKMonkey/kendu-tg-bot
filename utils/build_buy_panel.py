# formatters/build_buy_panel.py

from core.constants import (
    ETH_LP_ADDRESS, ETH_TOKEN_ADDRESS,
    BASE_LP_ADDRESS, BASE_TOKEN_ADDRESS,
    SOL_LP_ADDRESS, SOL_TOKEN_ADDRESS
)


def build_eth_buy_panel(buy: dict) -> str:
    tx = buy["tx_hash"]
    return (
        f"🛒 <b>NEW BUY!</b>\n\n"
        f"🐶 <b>Kendu Inu Buy on Ethereum</b>\n"
        f"{buy['emoji_row']}\n\n"
        f"💸 <b>Spent:</b> ${buy['amount_usd']} ({buy['amount_native']} ETH)\n"
        f"🪙 <b>Got:</b> {buy['tokens']} KENDU\n"
        f"📈 <b>Market Cap:</b> ${buy['market_cap']}\n"
        f"🔗 <a href='https://etherscan.io/tx/{tx}'>View TX</a>\n"
        f"📊 <a href='https://www.geckoterminal.com/ethereum/pools/{ETH_LP_ADDRESS}'>DexT</a> | "
        f"<a href='https://dexscreener.com/ethereum/{ETH_LP_ADDRESS}'>Screener</a> | "
        f"<a href='https://app.uniswap.org/swap?outputCurrency={ETH_TOKEN_ADDRESS}'>Buy</a> | "
        f"<a href='https://trending.kendu.io'>Trending</a>"
    )


def build_base_buy_panel(buy: dict) -> str:
    tx = buy["tx_hash"]
    return (
        f"🛒 <b>NEW BUY!</b>\n\n"
        f"🐶 <b>Kendu Inu Buy on Base</b>\n"
        f"{buy['emoji_row']}\n\n"
        f"💸 <b>Spent:</b> ${buy['amount_usd']} ({buy['amount_native']} ETH)\n"
        f"🪙 <b>Got:</b> {buy['tokens']} KENDU\n"
        f"📈 <b>Market Cap:</b> ${buy['market_cap']}\n"
        f"🔗 <a href='https://basescan.org/tx/{tx}'>View TX</a>\n"
        f"📊 <a href='https://www.geckoterminal.com/base/pools/{BASE_LP_ADDRESS}'>DexT</a> | "
        f"<a href='https://dexscreener.com/base/{BASE_LP_ADDRESS}'>Screener</a> | "
        f"<a href='https://app.uniswap.org/swap?chain=base&outputCurrency={BASE_TOKEN_ADDRESS}'>Buy</a> | "
        f"<a href='https://trending.kendu.io'>Trending</a>"
    )


def build_sol_buy_panel(buy: dict) -> str:
    tx = buy["tx_hash"]
    return (
        f"🛒 <b>NEW BUY!</b>\n\n"
        f"🐶 <b>Kendu Inu Buy on Solana</b>\n"
        f"{buy['emoji_row']}\n\n"
        f"💸 <b>Spent:</b> ${buy['amount_usd']} ({buy['amount_native']} SOL)\n"
        f"🪙 <b>Got:</b> {buy['tokens']} KENDU\n"
        f"📈 <b>Market Cap:</b> ${buy['market_cap']}\n"
        f"🔗 <a href='https://solscan.io/tx/{tx}'>View TX</a>\n"
        f"📊 <a href='https://www.geckoterminal.com/solana/pools/{SOL_LP_ADDRESS}'>DexT</a> | "
        f"<a href='https://dexscreener.com/solana/{SOL_LP_ADDRESS}'>Screener</a> | "
        f"<a href='https://trending.kendu.io'>Trending</a>"
    )
