import asyncio
import json
import os
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
WSS_BASE = os.getenv("WSS_BASE")
web3 = Web3(Web3.WebsocketProvider(WSS_BASE))
TRANSFER_TOPIC = web3.keccak(text="Transfer(address,address,uint256)").hex()
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

async def run_base_buy_watcher(bot):
    print("👀 Base buy watcher (Web3) started")

    # 1. ✅ WebSocket connection check
    if not web3.is_connected():
        print("❌ Failed to connect to Web3 for Base")
        return
    print("✅ Connected to Base WebSocket!")

    try:
        # 2. Convert to checksum format safely
        base_lp = Web3.to_checksum_address(BASE_LP_ADDRESS)
        base_token = Web3.to_checksum_address(BASE_TOKEN_ADDRESS)

        # 3. Validate contract addresses
        if web3.eth.get_code(base_token) == b'':
            print(f"❌ Base token address is invalid: {base_token}")
        else:
            print(f"✅ Base token address is valid: {base_token}")

        if web3.eth.get_code(base_lp) == b'':
            print(f"❌ Base LP address is invalid: {base_lp}")
        else:
            print(f"✅ Base LP address is valid: {base_lp}")

    except Exception as e:
        print(f"❌ Address checksum/validation failed: {e}")
        return

    # 4. 🧪 Filter creation test
    print("🧪 Testing Base filter...")
    try:
        event_filter = web3.eth.filter({
            "address": base_token,
            "topics": [TRANSFER_TOPIC]
        })
        print("✅ Base filter created successfully!")
    except Exception as e:
        print(f"❌ Base filter creation failed: {e}")
        return

    print("🚨 Base buy listener active!")
    buys = load_buys()

    def handle_event(log):
        try:
            topics = log["topics"]
            if topics[0].hex() != TRANSFER_TOPIC:
                return

            from_addr = Web3.to_checksum_address("0x" + topics[1].hex()[-40:])
            to_addr = Web3.to_checksum_address("0x" + topics[2].hex()[-40:])

            if from_addr.lower() != base_lp.lower():
                return

            token_amount = int(log["data"], 16)
            tokens = token_amount // (10**9)  # Adjust decimals if needed
            now = datetime.now(timezone.utc)

            buy = {
                "timestamp": now.isoformat(),
                "chain": "BASE",
                "amount_usd": 0,
                "amount_native": 0,
                "tokens": tokens,
                "market_cap": 0,
                "tx_hash": log["transactionHash"].hex(),
                "emoji_row": "🦍",
            }

            print(f"💰 New BASE Buy via Web3: {tokens:,} KENDU")
            buys.append(buy)
            save_buys(prune_old_buys(buys))

            msg = build_base_buy_panel(buy)
            asyncio.create_task(bot.send_message(
                chat_id=CHAT_ID,
                text=msg,
                parse_mode="HTML",
                disable_web_page_preview=True
            ))
        except Exception as e:
            print(f"⚠️ Web3 event handler error (BASE): {e}")

    # 5. 🔁 Poll loop
    while True:
        try:
            for log in event_filter.get_new_entries():
                handle_event(log)
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
        except Exception as e:
            print(f"⚠️ BASE Web3 loop error: {e}")
            await asyncio.sleep(10)
