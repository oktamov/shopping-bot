import os
import django
from aiogram import types

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Category, Product, Cart, Order
import pytz
from asgiref.sync import sync_to_async

from users.models import User


@sync_to_async
def start_cmd(message: types.Message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # Foydalanuvchini bazadan topib olish yoki yangi foydalanuvchini yaratish:
    user, created = User.objects.get_or_create(telegram_id=telegram_id)

    # Foydalanuvchi ma'lumotlarini yangilash:
    user.username = username
    user.first_name = first_name
    user.last_name = last_name
    user.save()


@sync_to_async
def find_user(telegram_id):
    user = User.objects.get(telegram_id=telegram_id)
    return user


def format_datetime_to_local(dt):
    local_timezone = pytz.timezone(pytz.country_timezones['UZ'][0])

    local_dt = dt.astimezone(local_timezone)

    return local_dt.strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')


@sync_to_async
def get_categories_list():
    categories = Category.objects.all()
    result = {}
    for category in categories:
        result[category.id] = category.name

    return result


@sync_to_async
def get_products_list(category):
    products = Product.objects.filter(category=category)
    result = {}
    for product in products:
        result[product.id] = product.name
    return result


@sync_to_async
def get_product(product):
    product = Product.objects.get(id=product)
    result = {}
    result['id'] = product.id
    result['name'] = product.name
    result['category'] = product.category.name
    result['category_id'] = product.category.id
    result['price'] = product.price
    result['count'] = product.count
    result['created_at'] = format_datetime_to_local(product.created_at).split(' ')[0]
    result['image'] = f"D:/Roziali/Projects/shopping-bot/media/{product.image.name}"
    result['description'] = product.description

    return result


@sync_to_async
def cart_create(message, product, price, quantity):
    try:

        user = User.objects.get(telegram_id=message.from_user.id)
        product = Product.objects.get(id=product)
        cart = Cart.objects.create(user=user, product=product, price=price, quantity=quantity)
        return cart
    except Exception as e:
        print(str(e))


@sync_to_async
def cart_delete(user, product):
    user = User.objects.get(telegram_id=user.from_user.id)
    product = Product.objects.get(id=product)
    cart = Cart.objects.get(user=user, product=product)
    cart.delete()


@sync_to_async
def all_cart_delete(user):
    user = User.objects.get(telegram_id=user.from_user.id)
    carts = Cart.objects.filter(user=user)
    carts.delete()


@sync_to_async
def user_cart(message):
    user = User.objects.get(telegram_id=message.from_user.id)
    carts = Cart.objects.filter(user=user, order__isnull=True)
    result = {}
    for cart in carts:
        result[cart.product.id] = cart.product.name
    return result


@sync_to_async
def order_create(user, name, phone, address):
    user = User.objects.get(telegram_id=user.from_user.id)

    order = Order.objects.create(user=user, name=name, phone=phone, address=address)
    carts = Cart.objects.filter(user=user, order__isnull=True)
    carts.update(order=order)

    return order


@sync_to_async
def one_order_create(user, name, phone, address, product):
    user = User.objects.get(telegram_id=user.from_user.id)
    product = Product.objects.get(id=product)
    cart = Cart.objects.create(user=user, product=product, quantity=1)
    order = Order.objects.create(user=user, name=name, phone=phone, address=address)
    cart.order = order
    cart.save()

    return order
