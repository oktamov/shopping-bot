from aiogram import types
from aiogram.types import CallbackQuery

from bot.keyboards.inline.extra import generate_carts_keyboard
from bot.loader import dp, bot
from bot.utils.functions import cart_create


@dp.callback_query_handler(lambda c: c.data.startswith('cart-create'))
async def show_products(call: CallbackQuery):
    product_id = call.data.split(' ')[1]
    price = call.data.split(' ')[2]
    cart_create(model=call.message, product=product_id, price=price, quantity=1)
    await call.message.answer("Mahsulot savatchaga qo'shildi.")


@dp.message_handler(lambda c: c.data.startswith('Savatcha 🛒'))
async def show_cart_list(message: types.Message):
    await message.answer("sizning savatchangizdagi mahsulotlar", reply_markup=await generate_carts_keyboard(message))
