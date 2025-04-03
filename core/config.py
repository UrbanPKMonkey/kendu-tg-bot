# core/config.py

import os
from dotenv import load_dotenv
from core import constants

# 🌱 Load .env variables
load_dotenv()

# === Telegram Config ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = constants.CHAT_ID

# === WebSocket / API Endpoints ===
WSS_ETH = os.getenv("WSS_ETH")  # e.g. wss://mainnet.infura.io/ws/v3/your_key

# === Liquidity Pools ===
ETH_LP_ADDRESS = constants.ETH_LP_ADDRESS
SOL_LP_ADDRESS = constants.SOL_LP_ADDRESS
BASE_LP_ADDRESS = constants.BASE_LP_ADDRESS

# === Token Addresses ===
ETH_TOKEN_ADDRESS = constants.ETH_TOKEN_ADDRESS
BASE_TOKEN_ADDRESS = constants.BASE_TOKEN_ADDRESS
SOL_TOKEN_ADDRESS = constants.SOL_TOKEN_ADDRESS

# === Polling & Timing ===
POLL_INTERVAL_SECONDS = constants.POLL_INTERVAL_SECONDS
RETENTION_PERIOD_HOURS = constants.RETENTION_PERIOD_HOURS

# === Emoji Logic ===
EMOJI_UNIT_USD = constants.EMOJI_UNIT_USD
MAX_EMOJIS = constants.MAX_EMOJIS

# === .env Validation Helper ===
REQUIRED_ENV_VARS = ["BOT_TOKEN", "WSS_ETH", "RAILWAY_PUBLIC_DOMAIN"]

def validate_env_vars():
    missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"❌ Missing required .env variables: {', '.join(missing)}")
