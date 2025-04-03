import asyncio
import json
import os
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
WSS_ETH = os.getenv("WSS_ETH")

web3 = Web3(Web3.WebsocketProvider(WSS_ETH))
TRANSFER_TOPIC = web3.keccak(text="Transfer(address,address,uint256)").hex()
JSON_LOG = "buys_eth.json"

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
    print("👀 Ethereum buy watcher (Web3) started")

    # 1. ✅ Test WebSocket connection
    if not web3.is_connected():
        print("❌ Failed to connect to Web3 for Ethereum")
        return
    print("✅ Connected to Ethereum WebSocket!")

    try:
        # 2. 🔁 Convert to checksum format (using local vars to avoid shadowing)
        eth_lp = Web3.to_checksum_address(ETH_LP_ADDRESS)
        eth_token = Web3.to_checksum_address(ETH_TOKEN_ADDRESS)

        # 3. ✅ Check on-chain validity
        if web3.eth.get_code(eth_token) == b'':
            print(f"❌ Ethereum token address is invalid: {eth_token}")
        else:
            print(f"✅ Ethereum token address is valid: {eth_token}")

        if web3.eth.get_code(eth_lp) == b'':
            print(f"❌ Ethereum LP address is invalid: {eth_lp}")
        else:
            print(f"✅ Ethereum LP address is valid: {eth_lp}")

    except Exception as e:
        print(f"❌ Address checksum/validation failed: {e}")
        return

    # 4. 🧪 Test filter creation
    print("🧪 Testing Ethereum filter...")
    try:
        event_filter = web3.eth.filter({
            "address": eth_token,
            "topics": [TRANSFER_TOPIC]
        })
        print("✅ Ethereum filter created successfully!")
    except Exception as e:
        print(f"❌ Ethereum filter creation failed: {e}")
        return

    print("🚨 Ethereum buy listener active!")
    buys = load_buys()

    def handle_event(log):
        try:
            topics = log["topics"]
            if topics[0].hex() != TRANSFER_TOPIC:
                return

            from_addr = Web3.to_checksum_address("0x" + topics[1].hex()[-40:])
            to_addr = Web3.to_checksum_address("0x" + topics[2].hex()[-40:])

            # ✅ Detect buys: from LP → user
            if from_addr.lower() != eth_lp.lower():
                return

            token_amount = int(log["data"], 16)
            tokens = token_amount // (10**9)  # Adjust decimals here if needed
            now = datetime.now(timezone.utc)

            buy = {
                "timestamp": now.isoformat(),
                "chain": "ETH",
                "amount_usd": 0,
                "amount_native": 0,
                "tokens": tokens,
                "market_cap": 0,
                "tx_hash": log["transactionHash"].hex(),
                "emoji_row": "🦍",
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

    # 5. 🎯 Poll loop
    while True:
        try:
            for log in event_filter.get_new_entries():
                handle_event(log)
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
        except Exception as e:
            print(f"⚠️ ETH Web3 loop error: {e}")
            await asyncio.sleep(10)
