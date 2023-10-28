import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery, InputFile

from loader import dp

from keyboards.default.main import get_main_keyboard

from keyboards.inline.category import generate_category_keyboard

from keyboards.inline.extra import product_detail_keyboard, generate_carts_keyboard
from keyboards.inline.product import generate_products_keyboard
from loader import bot

from bot.data.config import ADMINS
from bot.keyboards.inline.extra import generate_keyboard
from bot.keyboards.inline.product import generate_order_products_keyboard, generate_order_products_keyboard_for_admins
from bot.states.order import OrderForm, OneOrderForm
from bot.utils.functions import get_product, start_cmd, cart_delete, all_cart_delete, user_cart, \
    order_create, one_order_create, user_order_products, order_carts

from bot.utils.functions import cart_create


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await start_cmd(message)
    await message.answer(f"Salom, {message.from_user.full_name}! Botimizga xush kelibsiz!",
                         reply_markup=get_main_keyboard())


@dp.message_handler(lambda message: message.text == 'Mahsulotlar 🛍')
async def show_categories(message: types.Message):
    await message.answer("Kategoriylarni tanlang:", reply_markup=await generate_category_keyboard())


@dp.callback_query_handler(lambda c: c.data.startswith('back-to-category'))
async def back_categories(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    await call.message.answer("Kategoriylarni tanlang:", reply_markup=await generate_category_keyboard())


@dp.callback_query_handler(lambda c: c.data.startswith('back-to-products'))
async def back_categories(call: CallbackQuery):
    category_id = call.data.split(' ')[1]
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    await call.message.answer("Mahsulotlar:", reply_markup=await generate_products_keyboard(category_id))


@dp.callback_query_handler(lambda c: c.data.startswith('category-'))
async def show_products(call: CallbackQuery):
    category_id = call.data.split('-')[1]
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    await call.message.answer("Mahsulotlar:", reply_markup=await generate_products_keyboard(category_id))


@dp.callback_query_handler(lambda c: c.data.startswith('product-'))
async def product_detail(call: CallbackQuery):
    product_id = call.data.split('-')[1]
    product = await get_product(product_id)

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    id = product.get('id')
    name = product.get('name')
    price = product.get('price')
    count = product.get('count')
    image_path = product.get('image')
    description = product.get('description')
    category = product.get('category')
    category_id = product.get('category_id')

    formatted_text = f"*{name}*\n"
    formatted_text += f"Narxi: {price} so'm\n"
    formatted_text += f"Mahsulot soni: {count}\n"
    formatted_text += f"Qo'shimcha: {description}"

    markup = types.InlineKeyboardMarkup()
    button_back = types.InlineKeyboardButton(text="Orqaga⬅️", callback_data=f"back-to-products {category_id}")
    button_cart = types.InlineKeyboardButton(text="savatchga🛒", callback_data=f"cart-create {id} {price}")
    button_order = types.InlineKeyboardButton(text="Sotib olish", callback_data=f"order-one-product {id}")
    markup.add(button_back, button_cart, button_order)

    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=InputFile(photo),
            caption=formatted_text,
            parse_mode=types.ParseMode.MARKDOWN,
            reply_markup=markup

        )


@dp.callback_query_handler(lambda c: c.data.startswith('cart-create'))
async def show_products(call: CallbackQuery):
    product_id = call.data.split(' ')[1]
    price = call.data.split(' ')[2]
    await call.message.answer("Nechta sotib olasiz",
                              reply_markup=await generate_keyboard(start=1, product=int(product_id)))


@dp.callback_query_handler(lambda c: c.data.startswith('next_') or c.data.startswith('prev_'))
async def paginate_numbers(callback_query: types.CallbackQuery):
    start = int(callback_query.data.split('_')[1])
    new_keyboard = generate_keyboard(start)

    await callback_query.message.edit_reply_markup(reply_markup=await new_keyboard)
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data.startswith('number-cart-create'))
async def paginate_numbers(callback_query: types.CallbackQuery):
    quantity = callback_query.data.split(' ')[1]
    product = callback_query.data.split(' ')[2]
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

    await cart_create(message=callback_query, product=product, quantity=int(quantity))

    await callback_query.message.answer("Mahsulot savatchaga qo'shildi")


@dp.message_handler(lambda message: message.text.startswith('Savatcha 🛒'))
async def show_cart_list(message: types.Message):
    if await user_cart(message):
        await message.answer("sizning savatchangizdagi mahsulotlar",
                             reply_markup=await generate_carts_keyboard(message))
    else:
        await message.answer("Sizning mahsulotingiz yo'q.")


@dp.callback_query_handler(lambda c: c.data.startswith('cart-detail'))
async def cart_product_detail(call: CallbackQuery):
    product_id = call.data.split(' ')[1]
    product = await get_product(product_id)

    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    id = product.get('id')
    name = product.get('name')
    price = product.get('price')
    count = product.get('count')
    image_path = product.get('image')
    description = product.get('description')
    category = product.get('category')
    category_id = product.get('category_id')

    formatted_text = f"Nomi: *{name}*\n"
    formatted_text += f"Narxi: {price} so'm\n"
    formatted_text += f"Mahsulot soni: {count}\n"
    formatted_text += f"Qo'shimcha: {description}"

    markup = types.InlineKeyboardMarkup()
    button_back = types.InlineKeyboardButton(text="Orqaga⬅️", callback_data=f"back-to-products {category_id}")
    button_cart = types.InlineKeyboardButton(text="savatchadan o'chirish", callback_data=f"cart-delete {id}")
    markup.add(button_back, button_cart)

    with open(image_path, 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=InputFile(photo),
            caption=formatted_text,
            parse_mode=types.ParseMode.MARKDOWN,
            reply_markup=markup

        )


@dp.callback_query_handler(lambda c: c.data.startswith('cart-delete'))
async def delete_cart(call: CallbackQuery):
    product_id = call.data.split(' ')[1]
    await cart_delete(user=call, product=product_id)
    await call.message.answer("Mahsulot savatchadan o'chirildi.")


@dp.callback_query_handler(lambda c: c.data.startswith('delete-all-cart'))
async def delete_all_carts(call: CallbackQuery):
    await all_cart_delete(user=call)
    await call.message.answer("Mahsulotlar savatchadan o'chirildi.")


@dp.callback_query_handler(lambda c: c.data.startswith('buy-from-cart'))
async def buy_product_from_cart(call: CallbackQuery):
    await call.message.answer("To'liq ism-sharifingizni kiriting:")
    await call.message.answer("Sotib olishni bekor qilish uchun /start bosing")
    await OrderForm.name.set()


@dp.message_handler(state=OrderForm.name)
async def process_name(message: types.Message, state: FSMContext):
    user_name = message.text
    if user_name == '/start':
        await message.answer("Buyurtmanigiz bekor qilindi")
        await state.finish()
        return
    await state.update_data(name=user_name)

    await message.answer("Endi telefon raqam kiriting:\n exp: +998911234567")
    await OrderForm.next()


@dp.message_handler(state=OrderForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    phone_number = message.text
    if phone_number == '/start':
        await message.answer("Buyurtmanigiz bekor qilindi")
        await state.finish()
        return
    if not re.match(r'^\+\d{7,14}$', phone_number):
        await message.answer(
            "Iltimos to'g'ri raqam kiriting!.")
        await OrderForm.phone.set()
    else:
        await state.update_data(phone=phone_number)
        await message.answer("Aniq manzil kiriting:\n Toshkent sh. Shayxontohur, Beruniy-3A")
        await OrderForm.next()


@dp.message_handler(state=OrderForm.address)
async def process_name(message: types.Message, state: FSMContext):
    user_address = message.text
    user_data = await state.get_data()
    user_name = user_data.get('name')
    phone_number = user_data.get('phone')
    order = await order_create(user=message, name=user_name, phone=phone_number, address=user_address)

    await message.answer(f"Sotib olganingiz uchun rahmat. Siz bilan admin bog'laadi")
    await bot.send_message(5956865690,
                           f"Foydalanuvchi {user_name} ({message.from_user.id})"
                           f"telefon: {phone_number} "
                           f"{user_address}", reply_markup=await generate_order_products_keyboard_for_admins(order))

    await state.finish()


@dp.callback_query_handler(lambda c: c.data.startswith('order-one-product'))
async def buy_product_from_cart(call: CallbackQuery, state: FSMContext):
    product_id = call.data.split(' ')[1]
    await state.update_data(product=product_id)
    await call.message.answer("To'liq ism-sharifingizni kiriting:")
    await call.message.answer("Sotib olishni bekor qilish uchun /start bosing")
    await OneOrderForm.name.set()


@dp.message_handler(state=OneOrderForm.name)
async def process_name(message: types.Message, state: FSMContext):
    user_name = message.text
    if user_name == '/start':
        await message.answer("Buyurtmanigiz bekor qilindi")
        await state.finish()
        return
    await state.update_data(name=user_name)

    await message.answer("Endi telefon raqam kiriting:\n exp: +998911234567")
    await OneOrderForm.next()


@dp.message_handler(state=OneOrderForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    phone_number = message.text
    if phone_number == '/start':
        await message.answer("Buyurtmanigiz bekor qilindi")
        await state.finish()
        return
    if not re.match(r'^\+\d{7,14}$', phone_number):
        await message.answer(
            "Iltimos to'g'ri raqam kiriting!.")
        await OrderForm.phone.set()
    else:
        await state.update_data(phone=phone_number)
        await message.answer("Aniq manzil kiriting:\n Toshkent sh. Shayxontohur, Beruniy-3A")
        await OneOrderForm.next()


@dp.message_handler(state=OneOrderForm.address)
async def process_name(message: types.Message, state: FSMContext):
    user_address = message.text
    user_data = await state.get_data()
    user_name = user_data.get('name')
    phone_number = user_data.get('phone')
    product = user_data.get('product')
    order = await one_order_create(user=message, name=user_name, phone=phone_number, address=user_address,
                                   product=product)
    await message.answer(f"Sotib olganingiz uchun rahmat. Siz bilan admin bog'laadi")

    await bot.send_message(5956865690,
                           f"Foydalanuvchi {user_name} ({message.from_user.id})"
                           f"telefon: {phone_number} "
                           f"{user_address}", reply_markup=await generate_order_products_keyboard_for_admins(order))

    await state.finish()


@dp.message_handler(lambda c: c.text.startswith("Sotib olinganlar"))
async def bought_products(message: types.Message):
    products = await user_order_products(message=message)
    if products:
        await message.answer(f"Sizning sotib olgan mahsulotlaringiz👇",
                             reply_markup=await generate_order_products_keyboard(message))
    else:
        await message.answer(f"Sizning sotib olgan mahsulotingiz yoq")
