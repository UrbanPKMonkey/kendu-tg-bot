# watcher_base.py

import json
import os
import asyncio
from datetime import datetime, timedelta, timezone
from web3 import Web3
from dotenv import load_dotenv

from core.constants import (
    CHAT_ID,
    BASE_LP_ADDRESS,
    BASE_TOKEN_ADDRESS,
    POLL_INTERVAL_SECONDS,
    RETENTION_PERIOD_HOURS,
    EMOJI_UNIT_USD,
    MAX_EMOJIS
)
from utils.build_buy_panel import build_base_buy_panel

load_dotenv()
INFURA_HTTP_BASE = os.getenv("INFURA_HTTP_BASE")  # Add this to your .env

web3 = Web3(Web3.HTTPProvider(INFURA_HTTP_BASE))

JSON_LOG = "buys_base.json"
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

def build_filter_params(start_block, end_block):
    return {
        "fromBlock": start_block,
        "toBlock": end_block,
        "address": Web3.to_checksum_address(BASE_TOKEN_ADDRESS),
        "topics": [TRANSFER_TOPIC],
    }

async def run_base_buy_watcher(bot):
    print("👀 Base buy watcher (Polling) started")

    if not web3.is_connected():
        print("❌ Failed to connect to Base RPC")
        return

    print("✅ Connected to Base RPC!")
    buys = load_buys()

    BASE_LP = Web3.to_checksum_address(BASE_LP_ADDRESS)
    last_checked_block = web3.eth.block_number

    while True:
        try:
            latest_block = web3.eth.block_number
            if latest_block == last_checked_block:
                await asyncio.sleep(POLL_INTERVAL_SECONDS)
                continue

            logs = web3.eth.get_logs(build_filter_params(last_checked_block + 1, latest_block))

            for log in logs:
                topics = log["topics"]
                if topics[0].hex() != TRANSFER_TOPIC:
                    continue

                from_addr = Web3.to_checksum_address("0x" + topics[1].hex()[-40:])
                to_addr = Web3.to_checksum_address("0x" + topics[2].hex()[-40:])

                if from_addr.lower() != BASE_LP.lower():
                    continue

                token_amount = int(log["data"], 16)
                tokens = token_amount // (10**9)
                block = web3.eth.get_block(log["blockNumber"])
                ts = datetime.fromtimestamp(block["timestamp"], tz=timezone.utc)

                amount_usd = 0  # Placeholder
                amount_native = 0
                market_cap = 0
                emoji_row = "🦍"

                buy = {
                    "timestamp": ts.isoformat(),
                    "chain": "BASE",
                    "amount_usd": amount_usd,
                    "amount_native": amount_native,
                    "tokens": tokens,
                    "market_cap": market_cap,
                    "tx_hash": log["transactionHash"].hex(),
                    "emoji_row": emoji_row,
                }

                print(f"💰 New BASE Buy via Polling: {tokens:,} KENDU")
                buys.append(buy)
                save_buys(prune_old_buys(buys))

                msg = build_base_buy_panel(buy)
                await bot.send_message(
                    chat_id=CHAT_ID,
                    text=msg,
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )

            last_checked_block = latest_block
            await asyncio.sleep(POLL_INTERVAL_SECONDS)

        except Exception as e:
            print(f"⚠️ BASE polling error: {e}")
            await asyncio.sleep(10)
