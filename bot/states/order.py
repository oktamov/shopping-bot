from aiogram.dispatcher.filters.state import State, StatesGroup


class OrderForm(StatesGroup):
    name = State()
    phone = State()
    address = State()


class OneOrderForm(StatesGroup):
    products = State()
    name = State()
    phone = State()
    address = State()
