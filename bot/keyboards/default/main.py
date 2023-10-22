from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    mahsulotlar_btn = KeyboardButton("Mahsulotlar 🛍")
    savatcha_btn = KeyboardButton("Savatcha 🛒")
    sotib_olinganlar_btn = KeyboardButton("Sotib olinganlar")

    markup.add(mahsulotlar_btn, savatcha_btn, sotib_olinganlar_btn)
    return markup
