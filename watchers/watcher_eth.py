# watcher_eth.py

import json
import os
import asyncio
from datetime import datetime, timedelta, timezone
from web3 import Web3
from dotenv import load_dotenv

from core.constants import (
    CHAT_ID,
    ETH_LP_ADDRESS,
    ETH_TOKEN_ADDRESS,
    POLL_INTERVAL_SECONDS,
    RETENTION_PERIOD_HOURS,
    EMOJI_UNIT_USD,
    MAX_EMOJIS
)
from utils.build_buy_panel import build_eth_buy_panel

load_dotenv()
INFURA_WSS = os.getenv("INFURA_WSS")
web3 = Web3(Web3.WebsocketProvider(INFURA_WSS))

JSON_LOG = "buys_eth.json"
TRANSFER_TOPIC = web3.keccak(text="Transfer(address,address,uint256)").hex()


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


async def run_eth_buy_watcher(bot):
    print("👀 ETH buy watcher (Web3) started")
    buys = load_buys()

    if not web3.is_connected():
        print("❌ Failed to connect to Web3")
        return

    def handle_event(log):
        try:
            topics = log["topics"]
            if topics[0].hex() != TRANSFER_TOPIC:
                return

            from_addr = Web3.to_checksum_address("0x" + topics[1].hex()[-40:])
            if from_addr.lower() != ETH_LP_ADDRESS.lower():
                return

            token_amount = int(log["data"], 16)
            tokens = token_amount // 10**9
            now = datetime.now(timezone.utc)

            # Placeholder values
            amount_usd = 0
            amount_native = 0
            market_cap = 0
            emoji_row = "🦍"

            buy = {
                "timestamp": now.isoformat(),
                "chain": "ETH",
                "amount_usd": amount_usd,
                "amount_native": amount_native,
                "tokens": tokens,
                "market_cap": market_cap,
                "tx_hash": log["transactionHash"].hex(),
                "emoji_row": emoji_row,
            }

            print(f"💰 New ETH Buy via Web3: {tokens:,} KENDU")
            buys.append(buy)
            save_buys(prune_old_buys(buys))

            msg = build_eth_buy_panel(buy)
            asyncio.create_task(bot.send_message(
                chat_id=CHAT_ID,
                text=msg,
                parse_mode="HTML",
                disable_web_page_preview=True
            ))

        except Exception as e:
            print(f"⚠️ Web3 event handler error: {e}")

    # 👂 Subscribe to Transfer events
    event_filter = web3.eth.filter({
        "address": ETH_TOKEN_ADDRESS,
        "topics": [TRANSFER_TOPIC]
    })

    while True:
        try:
            for log in event_filter.get_new_entries():
                handle_event(log)
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
        except Exception as e:
            print(f"⚠️ ETH Web3 loop error: {e}")
            await asyncio.sleep(10)
