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

    # Test WebSocket connection
    if not web3.is_connected():
        print("❌ Failed to connect to Web3 for Ethereum")
        return

    print("✅ Connected to Ethereum WebSocket!")

    # Ensure checksum format for Ethereum LP and Token addresses
    try:
        ETH_LP_ADDRESS = Web3.to_checksum_address(ETH_LP_ADDRESS)  # Ensure checksum format
        ETH_TOKEN_ADDRESS = Web3.to_checksum_address(ETH_TOKEN_ADDRESS)  # Ensure checksum format
    except ValueError as e:
        print(f"❌ Error with addresses: {e}")
        return

    # Validate Ethereum token and LP addresses
    if web3.eth.get_code(ETH_TOKEN_ADDRESS) == b'':
        print(f"❌ Ethereum token address is invalid: {ETH_TOKEN_ADDRESS}")
    else:
        print(f"✅ Ethereum token address is valid: {ETH_TOKEN_ADDRESS}")
    
    if web3.eth.get_code(ETH_LP_ADDRESS) == b'':
        print(f"❌ Ethereum LP address is invalid: {ETH_LP_ADDRESS}")
    else:
        print(f"✅ Ethereum LP address is valid: {ETH_LP_ADDRESS}")

    buys = load_buys()

    def handle_event(log):
        try:
            topics = log["topics"]
            if topics[0].hex() != TRANSFER_TOPIC:
                return

            from_addr = Web3.to_checksum_address("0x" + topics[1].hex()[-40:])
            to_addr = Web3.to_checksum_address("0x" + topics[2].hex()[-40:])

            if from_addr.lower() != ETH_LP_ADDRESS.lower():
                return

            token_amount = int(log["data"], 16)
            tokens = token_amount // 10**9
            now = datetime.now(timezone.utc)

            amount_usd = 0  # Placeholder
            amount_native = 0  # Placeholder
            market_cap = 0  # Placeholder
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

    # 👂 Subscribe to Transfer events for KENDU token
    print("🧪 Testing Ethereum filter...")
    try:
        event_filter = web3.eth.filter({
            "address": ETH_TOKEN_ADDRESS,
            "topics": [TRANSFER_TOPIC]
        })
        print("✅ Ethereum filter created successfully!")
    except Exception as e:
        print(f"❌ Ethereum filter creation failed: {e}")
        return

    print("👀 Starting Ethereum buy watcher...")

    while True:
        try:
            for log in event_filter.get_new_entries():
                handle_event(log)
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
        except Exception as e:
            print(f"⚠️ ETH Web3 loop error: {e}")
            await asyncio.sleep(10)
