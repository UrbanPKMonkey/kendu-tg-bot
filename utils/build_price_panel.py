def build_price_panel(price_data: dict) -> str:
    price = price_data["price"]
    change_24h = price_data["change_24h"]
    volume_24h = price_data["volume_24h"]
    market_cap = price_data["market_cap"]
    gas_price = price_data["gas"]

    change_emoji = "🟢" if change_24h.startswith("+") else "🔴"

    return (
        "📊 $KENDU Live Price\n\n"
        f"• 🪙 Price: ${price}\n"
        f"• {change_emoji} 24H Change: {change_24h}\n"
        f"• 📦 24H Volume: ${volume_24h}\n"
        f"• 💰 Market Cap: ${market_cap}\n"
        f"• ⛽️ Gas: {gas_price} gwei (fast)"
    )
