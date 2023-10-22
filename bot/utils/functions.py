import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from products.models import Category, Product
import pytz
from asgiref.sync import sync_to_async


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
    result['price'] = product.price
    result['count'] = product.count
    result['created_at'] = format_datetime_to_local(product.created_at).split(' ')[0]
    result['image'] = f"D:/Roziali/Projects/shopping-bot/media/{product.image.name}"
    result['description'] = product.description

    return result


if __name__ == '__main__':
    print(get_product(2))
