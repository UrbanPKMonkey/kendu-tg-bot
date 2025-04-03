import time
import aiohttp
from datetime import datetime

GECKO_ETH_URL = "https://api.geckoterminal.com/api/v2/networks/eth/pools/0xd9f2a7471d1998c69de5cae6df5d3f070f01df9f"
BEACON_GAS_URL = "https://beaconcha.in/api/v1/execution/gasnow"

CACHE_DURATION = 60  # seconds
_price_cache = {}
_last_fetch_time = 0
_last_updated = None


async def get_latest_prices():
    global _price_cache, _last_fetch_time, _last_updated

    if time.time() - _last_fetch_time < CACHE_DURATION and _price_cache:
        print("✅ Returning cached price data")
        return _price_cache

    data_fetched = {}

    try:
        async with aiohttp.ClientSession() as session:
            # Fetch price from GeckoTerminal
            print("🔍 Getting price from GeckoTerminal...")
            async with session.get(GECKO_ETH_URL) as res:
                eth_data = await res.json()
                print("✅ Price fetched")

            pool_data = eth_data["data"]["attributes"]
            price_usd = float(pool_data["base_token_price_usd"])
            volume_24h = float(pool_data["volume_usd"]["h24"])
            price_change = float(pool_data["price_change_percentage"]["h24"])
            market_cap = float(pool_data["market_cap_usd"])

            data_fetched.update({
                "price": f"{price_usd:.6f}",
                "volume_24h": f"{volume_24h:,.0f}",
                "market_cap": f"{market_cap:,.0f}",
                "change_24h": f"{price_change:+.1f}%",
                "is_positive": price_change >= 0
            })

    except Exception as e:
        print(f"[price_fetcher] Error fetching ETH price: {e}")

    try:
        async with aiohttp.ClientSession() as session:
            # Fetch gas from Beaconcha.in
            print("🔍 Getting gas from Beaconcha.in...")
            async with session.get(BEACON_GAS_URL) as gas_res:
                gas_data = await gas_res.json()
                print("✅ Gas fetched")

            gas_standard_wei = gas_data["data"]["standard"]
            gas_standard_gwei = round(gas_standard_wei / 1_000_000_000)

            data_fetched["gas"] = gas_standard_gwei

    except Exception as e:
        print(f"[price_fetcher] Error fetching gas: {e}")
        data_fetched["gas"] = "⚠️ Unable to fetch gas"

    _price_cache = {"ETH": data_fetched}
    _last_fetch_time = time.time()
    _last_updated = datetime.utcnow()

    return _price_cache


def build_price_panel(data: dict) -> str:
    eth = data.get("ETH", {})
    if not eth or "price" not in eth:
        return "⚠️ Unable to fetch live price data."

    circle = "🟢" if eth.get("is_positive") else "🔴"
    gas = eth.get("gas", "⚠️ Unable to fetch gas")

    # Timestamp formatting
    updated_str = (
        _last_updated.strftime("%m/%d %H:%M UTC")
        if _last_updated else "Unknown"
    )

    return (
        f"📊 <b>$KENDU Price</b>\n\n"
        f"• <b>💲 Price:</b> ${eth.get('price', 'N/A')}\n"
        f"• <b>{circle} 24H Change:</b> {eth.get('change_24h', 'N/A')}\n"
        f"• <b>📦 24H Volume:</b> ${eth.get('volume_24h', 'N/A')}\n"
        f"• <b>🏦 Market Cap:</b> ${eth.get('market_cap', 'N/A')}\n"
        f"• <b>⛽️ Gas:</b> {gas} gwei (standard)\n\n"
        f"<i>⏰ Last Updated: {updated_str}</i>"
    )


async def get_kendu_price_panel():
    latest_prices = await get_latest_prices()
    return build_price_panel(latest_prices)
