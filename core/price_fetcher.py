import time
import aiohttp

GECKO_ETH_URL = "https://api.geckoterminal.com/api/v2/networks/eth/pools/0x416C8B26d8d18CE4Fa716350FE1C7Ddc1A479fb3"
BEACON_GAS_URL = "https://beaconcha.in/api/v1/execution/gasnow"

CACHE_DURATION = 60  # seconds
_price_cache = {}
_last_fetch_time = 0

async def get_latest_prices():
    global _price_cache, _last_fetch_time

    if time.time() - _last_fetch_time < CACHE_DURATION and _price_cache:
        return _price_cache

    try:
        async with aiohttp.ClientSession() as session:
            # Get ETH price and volume from GeckoTerminal
            async with session.get(GECKO_ETH_URL) as res:
                eth_data = await res.json()

            # Get gas from Beaconcha.in (GasNow)
            async with session.get(BEACON_GAS_URL) as gas_res:
                gas_data = await gas_res.json()

        # Parse GeckoTerminal response
        pool_data = eth_data["data"]["attributes"]
        price_usd = float(pool_data["base_token_price_usd"])
        volume_24h = float(pool_data["volume_usd"]["h24"])
        price_change = float(pool_data["price_change_percentage"]["h24"])
        market_cap = float(pool_data["base_token_market_cap_usd"])

        # Parse GasNow response from Beaconcha.in
        gas_fast_wei = gas_data["data"]["fast"]
        gas_fast_gwei = gas_fast_wei / 1_000_000_000

        # Store formatted ETH data
        _price_cache = {
            "ETH": {
                "price": f"{price_usd:.6f}",
                "volume_24h": f"{volume_24h:,.0f}",
                "market_cap": f"{market_cap:,.0f}",
                "change_24h": f"{price_change:+.1f}%",
                "gas": f"{gas_fast_gwei:.0f}",
                "is_positive": price_change >= 0
            }
        }
        _last_fetch_time = time.time()

        return _price_cache

    except Exception as e:
        print(f"[price_fetcher] Error fetching ETH price or gas: {e}")
        return {}
