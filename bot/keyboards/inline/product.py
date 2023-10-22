from aiogram import types

from utils.functions import get_products_list


async def generate_products_keyboard(category):
    markup = types.InlineKeyboardMarkup()
    products = await get_products_list(category)
    for product_id, product_name in products.items():
        button = types.InlineKeyboardButton(text=product_name, callback_data=f"product-{product_id}")
        markup.add(button)
    return markup


