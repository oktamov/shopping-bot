from aiogram import types

from utils.functions import get_categories_list


async def generate_category_keyboard():
    markup = types.InlineKeyboardMarkup()
    categories = await get_categories_list()
    for category_id, category_name in categories.items():
        button = types.InlineKeyboardButton(text=f"{category_name}", callback_data=f"category-{category_id}")
        markup.add(button)
    return markup
