from aiogram import types

from utils.functions import get_products_list

from bot.utils.functions import user_order_products, order_carts


async def generate_products_keyboard(category):
    markup = types.InlineKeyboardMarkup()
    products = await get_products_list(category)
    for product_id, product_name in products.items():
        button = types.InlineKeyboardButton(text=product_name, callback_data=f"product-{product_id}")
        markup.add(button)
    back_button = types.InlineKeyboardButton(text="Orqaga⬅️", callback_data="back-to-category")
    markup.add(back_button)
    return markup


async def generate_order_products_keyboard(message):
    markup = types.InlineKeyboardMarkup()
    products = await user_order_products(message=message)
    for product_id, product_name in products.items():
        button = types.InlineKeyboardButton(text=product_name, callback_data=f"product-{product_id}")
        markup.add(button)
    back_button = types.InlineKeyboardButton(text="Orqaga⬅️", callback_data="back-to-category")
    markup.add(back_button)
    return markup


async def generate_order_products_keyboard_for_admins(order):
    markup = types.InlineKeyboardMarkup()
    products = await order_carts(order)
    print(products)
    for product in products:
        print(product)
        button = types.InlineKeyboardButton(text=f"{product.get('name')} - {product.get('soni')}", callback_data=f"product-{product.get('id')}")
        markup.add(button)
    back_button = types.InlineKeyboardButton(text="Orqaga⬅️", callback_data="back-to-category")
    markup.add(back_button)
    return markup
