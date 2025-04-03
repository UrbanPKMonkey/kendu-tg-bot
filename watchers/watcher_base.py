# watcher_base.py

import asyncio
import json
import os
import aiohttp
from datetime import datetime, timedelta, timezone

from core.constants import (
    CHAT_ID,
    BASE_LP_ADDRESS,
    POLL_INTERVAL_SECONDS,
    RETENTION_PERIOD_HOURS,
    EMOJI_UNIT_USD,
    MAX_EMOJIS
)
from utils.build_buy_panel import build_base_buy_panel

GECKO_URL = f"https://api.geckoterminal.com/api/v2/networks/base/pools/{BASE_LP_ADDRESS}/swaps"
JSON_LOG = "buys_base.json"


def load_buys():
    if os.path.exists(JSON_LOG):
        with open(JSON_LOG, "r") as f:
            return json.load(f)
    return []


def save_buys(data):
    with open(JSON_LOG, "w") as f:
        json.dump(data, f, indent=2)


def prune_old_buys(data):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=RETENTION_PERIOD_HOURS)
    return [b for b in data if datetime.fromisoformat(b["timestamp"]) >= cutoff]


async def fetch_latest_swaps():
    async with aiohttp.ClientSession() as session:
        async with session.get(GECKO_URL) as resp:
            data = await resp.json()
            return data["data"]["attributes"]["swaps"]


async def run_base_buy_watcher(bot):
    print("👀 BASE buy watcher started")
    seen_tx_ids = set()
    buys = load_buys()

    while True:
        try:
            swaps = await fetch_latest_swaps()
            new_detected = []

            for s in swaps:
                if s["trade_type"] != "buy":
                    continue

                tx = s["tx_id"]
                if tx in seen_tx_ids:
                    continue

                seen_tx_ids.add(tx)
                ts = datetime.fromtimestamp(s["timestamp"], tz=timezone.utc)

                amount_usd = round(float(s["amount_in_usd"]), 2)
                amount_native = round(float(s["amount_in"]), 4)
                tokens = int(float(s["amount_out"]))
                market_cap = int(float(s.get("market_cap_usd", 0)))
                emoji_row = "🦍" * min(max(int(amount_usd / EMOJI_UNIT_USD), 1), MAX_EMOJIS)

                buy = {
                    "timestamp": ts.isoformat(),
                    "chain": "BASE",
                    "amount_usd": amount_usd,
                    "amount_native": amount_native,
                    "tokens": tokens,
                    "market_cap": market_cap,
                    "tx_hash": tx,
                    "emoji_row": emoji_row
                }

                print(f"💰 New BASE Buy: ${amount_usd} | {tokens} KENDU")
                buys.append(buy)
                new_detected.append(buy)

            if new_detected:
                buys = prune_old_buys(buys)
                save_buys(buys)

                for buy in new_detected:
                    msg = build_base_buy_panel(buy)
                    await bot.send_message(
                        chat_id=CHAT_ID,
                        text=msg,
                        parse_mode="HTML",
                        disable_web_page_preview=True
                    )

            await asyncio.sleep(POLL_INTERVAL_SECONDS)

        except Exception as e:
            print(f"⚠️ BASE watcher error: {e}")
            await asyncio.sleep(10)
