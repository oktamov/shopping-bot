from django.db import models


class User(models.Model):
    telegram_id = models.PositiveBigIntegerField(unique=True, verbose_name="Telegram ID")
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    last_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Last Name")

    def __str__(self):
        return f"{self.first_name} ({self.telegram_id})"
