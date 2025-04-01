from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from io import BytesIO
import requests
from PIL import Image

def get_contracts_text_and_markup():
    text = (
        "🧾 <b>Contract Addresses</b>\n\n"
        "⚫ <b>Ethereum (ETH):</b>\n"
        "<code>   0xaa95f26e30001251fb905d264Aa7b00eE9dF6C18</code>\n\n"
        "🟣 <b>Solana (SOL):</b>\n"
        "<code>   2nnrviYJRLcf2bXAxpKTRXzccoDbwaP4vzuGUG75Jo45</code>\n\n"
        "🔵 <b>Base (BASE):</b>\n"
        "<code>   0xef73611F98DA6E57e0776317957af61B59E09Ed7</code>"
    )
    markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="menu")]])
    return text, markup

async def add_black_background_to_image(image_url: str) -> BytesIO:
    response = requests.get(image_url)
    original = Image.open(BytesIO(response.content)).convert("RGBA")
    background = Image.new("RGB", original.size, (0, 0, 0))
    background.paste(original, mask=original.split()[3])
    output = BytesIO()
    output.name = "with_black_bg.png"
    background.save(output, format="PNG")
    output.seek(0)
    return output
