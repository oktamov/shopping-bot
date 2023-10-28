from aiogram import types

from bot.utils.functions import user_cart


async def product_detail_keyboard(category):
    markup = types.InlineKeyboardMarkup()
    button_back = types.InlineKeyboardButton(text="Orqaga⬅️", callback_data=f"back-to-products {category}")
    button_cart = types.InlineKeyboardButton(text="savatchga🛒", callback_data="cart-create")
    button_order = types.InlineKeyboardButton(text="Sotib olish", callback_data="order-product")
    markup.add(button_back, button_cart, button_order)
    return markup


async def generate_carts_keyboard(message):
    markup = types.InlineKeyboardMarkup()
    products = await user_cart(message)
    for product_id, product_name in products.items():
        button = types.InlineKeyboardButton(text=product_name, callback_data=f"cart-detail {product_id}")
        markup.add(button)
    buy_button = types.InlineKeyboardButton(text="Hammasini sotib olish", callback_data="buy-from-cart")
    markup.add(buy_button)
    delete_button = types.InlineKeyboardButton(text="Hammasini o'chirish", callback_data="delete-all-cart")
    markup.add(delete_button)
    return markup


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def generate_keyboard(start: int = 1, product: int = 1):
    markup = InlineKeyboardMarkup()

    for j in range(3):
        buttons = []
        for i in range(start + j * 3, start + j * 3 + 3):
            if i <= 100:
                buttons.append(InlineKeyboardButton(str(i), callback_data=f"number-cart-create {i} {product}"))
        markup.add(*buttons)

    navigation_buttons = []
    if start > 1:
        navigation_buttons.append(InlineKeyboardButton("⬅️ Oldin",
                                                       callback_data=f"prev_{start - 9}"))
    if start + 9 <= 100:
        navigation_buttons.append(InlineKeyboardButton("Keyingi ➡️", callback_data=f"next_{start + 9}"))

    markup.add(*navigation_buttons)

    return markup
