from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=55)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.FloatField(default=1)
    image = models.ImageField(upload_to='products/')
    count = models.IntegerField(default=1)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_viewed = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.user}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='cart', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_products')
    price = models.FloatField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} -> {self.product}"

    @property
    def total_price(self):
        cart_items = Cart.objects.filter(user=self.user, order=self.order)
        total = sum(item.price for item in cart_items)
        return total

    @property
    def total_quantity(self):
        cart_items = Cart.objects.filter(user=self.user, order=self.order)
        total = sum(item.quantity for item in cart_items)
        return total

    def save(self, *args, **kwargs):
        self.price = self.quantity * self.product.price
        super().save(*args, **kwargs)
