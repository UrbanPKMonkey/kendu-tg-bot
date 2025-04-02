import time
import aiohttp

# URLs
GECKO_ETH_URL = "https://api.geckoterminal.com/api/v2/networks/eth/pools/0x416C8B26d8d18CE4Fa716350FE1C7Ddc1A479fb3"
BEACON_GAS_URL = "https://beaconcha.in/api/v1/execution/gasnow"

# Cache settings
CACHE_DURATION = 60  # seconds
_price_cache = {}
_last_fetch_time = 0


async def get_latest_prices():
    global _price_cache, _last_fetch_time

    if time.time() - _last_fetch_time < CACHE_DURATION and _price_cache:
        return _price_cache

    try:
        async with aiohttp.ClientSession() as session:
            # Fetch ETH price and volume from GeckoTerminal
            async with session.get(GECKO_ETH_URL) as res:
                eth_data = await res.json()

            # Fetch gas price from Beaconcha.in
            async with session.get(BEACON_GAS_URL) as gas_res:
                gas_data = await gas_res.json()

        # Parse GeckoTerminal data
        pool_data = eth_data["data"]["attributes"]
        price_usd = float(pool_data["base_token_price_usd"])
        volume_24h = float(pool_data["volume_usd"]["h24"])
        price_change = float(pool_data["price_change_percentage"]["h24"])
        market_cap = float(pool_data["base_token_market_cap_usd"])

        # Format price data
        price_str = f"{price_usd:.6f}"
        volume_str = f"{volume_24h:,.0f}"
        market_cap_str = f"{market_cap:,.0f}"
        change_str = f"{price_change:+.1f}%"

        # Parse and convert gas data from Beaconcha.in
        gas_fast_wei = gas_data["data"]["fast"]
        gas_fast_gwei = round(gas_fast_wei / 1_000_000_000)

        # Cache ETH data
        _price_cache = {
            "ETH": {
                "price": price_str,
                "volume_24h": volume_str,
                "market_cap": market_cap_str,
                "change_24h": change_str,
                "gas": gas_fast_gwei,
                "is_positive": price_change >= 0
            }
        }
        _last_fetch_time = time.time()

        return _price_cache

    except Exception as e:
        print(f"[price_fetcher] Error fetching ETH price or gas: {e}")
        return {}


def build_price_panel(data: dict) -> str:
    eth = data.get("ETH", {})
    if not eth:
        return "⚠️ Unable to fetch live price data."

    # Determine circle emoji color based on price change
    circle = "🟢" if eth.get("is_positive") else "🔴"

    return (
        f"\n\n📊 $KENDU Live Price\n"
        f"• 🪙 Price: ${eth['price']}\n"
        f"• {circle} 24H Change: {eth['change_24h']}\n"
        f"• 📦 24H Volume: ${eth['volume_24h']}\n"
        f"• 💰 Market Cap: ${eth['market_cap']}\n"
        f"• ⛽️ Gas: {eth['gas']} gwei (fast)"
    )


async def get_kendu_price_panel():
    latest_prices = await get_latest_prices()
    return build_price_panel(latest_prices)
