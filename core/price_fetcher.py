import httpx
import time

# ✅ Token + gas API endpoints
API_ENDPOINTS = {
    "eth": "https://api.geckoterminal.com/api/v2/networks/eth/tokens/0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18",
    "sol": "https://api.geckoterminal.com/api/v2/networks/solana/tokens/2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45",
    "base": "https://api.geckoterminal.com/api/v2/networks/base/tokens/0xef73611F98DA6E57e0776317957af61B59E09Ed7",
}
ETH_GAS_API = "https://api.etherscan.io/api?module=gastracker&action=gasoracle"

# ✅ In-memory cache
_price_cache = {"data": None, "timestamp": 0}
CACHE_DURATION = 60  # seconds


def format_number(num: float) -> str:
    if num >= 1_000_000_000:
        return f"${num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"${num / 1_000_000:.2f}M"
    else:
        return f"${num:,.0f}"


def format_percent_change(change: float) -> str:
    sign = "+" if change >= 0 else "−"
    return f"{sign}{abs(change):.1f}% 24h"


def build_price_block(data: dict) -> str:
    text = (
        f"{data['emoji']} <b>{data['label']}</b>\n"
        f"Price: {data['price']} ({data['change']})\n"
        f"Market Cap: {data['market_cap']}"
    )
    if data.get("gas"):
        text += f"\nGas: {data['gas']}"
    return text + "\n"


async def get_eth_gas_fee() -> str:
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(ETH_GAS_API, timeout=10)
            res.raise_for_status()
            data = res.json()["result"]
            return f"{data['FastGasPrice']} gwei (fast)"
    except Exception as e:
        print(f"⚠️ Error fetching ETH gas fee: {e}")
        return "Unavailable"


async def get_kendu_price_panel() -> str:
    # ✅ Use cache if fresh
    now = time.time()
    if _price_cache["data"] and now - _price_cache["timestamp"] < CACHE_DURATION:
        print("💾 Using cached price panel")
        return _price_cache["data"]

    print("🌐 Fetching fresh prices...")
    output = ["📊 <b>$KENDU Live Prices</b>\n"]

    display_data = {
        "eth": {"emoji": "⚫", "label": "Ethereum (ETH)"},
        "sol": {"emoji": "🟣", "label": "Solana (SOL)"},
        "base": {"emoji": "🔵", "label": "Base (BASE)"},
    }

    eth_gas = await get_eth_gas_fee()

    async with httpx.AsyncClient() as client:
        for chain, url in API_ENDPOINTS.items():
            try:
                res = await client.get(url, timeout=10)
                res.raise_for_status()
                token_data = res.json()["data"]["attributes"]

                price = f"${float(token_data['price_usd']):.6f}"
                mcap = format_number(float(token_data['market_cap_usd']))
                change_24h = format_percent_change(float(token_data["price_percent_change_24h"]))

                display_data[chain]["price"] = price
                display_data[chain]["market_cap"] = mcap
                display_data[chain]["change"] = change_24h

                if chain == "eth":
                    display_data[chain]["gas"] = eth_gas

                output.append(build_price_block(display_data[chain]))

            except Exception as e:
                print(f"⚠️ Error fetching {chain.upper()} data: {e}")
                output.append(f"{display_data[chain]['emoji']} <b>{display_data[chain]['label']}</b>\nUnavailable\n")

    final_text = "\n".join(output)
    _price_cache["data"] = final_text
    _price_cache["timestamp"] = now

    return final_text
