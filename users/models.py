from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """
    Модель пользователя
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(max_length=35, verbose_name="телефон", **NULLABLE)
    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="аватар", **NULLABLE
    )
    city = models.CharField(max_length=50, verbose_name="город", **NULLABLE)
    token = models.CharField(max_length=100, verbose_name="token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    payment_choices = (("наличные", "наличные"), ("перевод на счет", "перевод на счет"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="пользователь"
    )
    payment_date = models.DateField(verbose_name="дата оплаты", auto_now_add=True)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, verbose_name="оплаченный курс", **NULLABLE
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="отдельно оплаченный урок",
        **NULLABLE
    )
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.CharField(max_length=100, choices=payment_choices)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ("payment_date",)


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="подписка пользователя"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="курс подписки"
    )
