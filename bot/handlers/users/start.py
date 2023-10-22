from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery, InputFile

from loader import dp

from keyboards.default.main import get_main_keyboard

from keyboards.inline.category import generate_category_keyboard

from bot.keyboards.inline.product import generate_products_keyboard
from bot.loader import bot
from bot.utils.functions import get_products_list, get_product


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=get_main_keyboard())


@dp.message_handler(lambda message: message.text == 'Mahsulotlar 🛍')
async def show_categories(message: types.Message):
    await message.answer("Kategoriylarni tanlang:", reply_markup=await generate_category_keyboard())


@dp.callback_query_handler(lambda c: c.data.startswith('category-'))
async def fanlar(call: CallbackQuery):
    category_id = call.data.split('-')[1]
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    await call.message.answer("Mahsulotlar:", reply_markup=await generate_products_keyboard(category_id))


@dp.callback_query_handler(lambda c: c.data.startswith('product-'))
async def process_category(call: CallbackQuery):
    product_id = call.data.split('-')[1]
    product = await get_product(product_id)

    # Xabarni o'chirish
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    name = product.get('name')
    price = product.get('price')
    count = product.get('count')
    image_path = product.get('image')  # bu yerda image_path - rasmning kompyuter xotirasidagi yo'li
    description = product.get('description')

    # Mahsulot malumotlarini chiroyli formatda yaratish
    formatted_text = f"*{name}*\n"
    formatted_text += f"Price: {price}\n"
    formatted_text += f"Available: {count}\n"
    formatted_text += f"_Description_: {description}"

    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=InputFile(photo),
            caption=formatted_text,
            parse_mode=types.ParseMode.MARKDOWN
        )