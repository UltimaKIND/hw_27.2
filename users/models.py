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
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="пользователь", **NULLABLE
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
    payment_amount = models.PositiveIntegerField(
        verbose_name="оплата", help_text="введите сумму оплаты", **NULLABLE
    )
    session_id = models.CharField(
        max_length=255,
        verbose_name="Id сессии",
        help_text="Укажите Id сессии",
        **NULLABLE
    )
    link = models.URLField(
        max_length=400,
        verbose_name="ссылка на оплату",
        help_text="Укажите ссылку на оплату",
        **NULLABLE
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ("payment_date",)

    def __str__(self):
        return self.payment_amount


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="подписка пользователя"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="курс подписки"
    )
