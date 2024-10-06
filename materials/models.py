from django.db import models
from users.models import User

# константа для полей с возможными нулевыми значениями
NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    """
    модель курса
    """

    title = models.CharField(max_length=100, verbose_name="название курса")
    preview = models.ImageField(
        upload_to="materials/preview", verbose_name="превью курса", **NULLABLE
    )
    description = models.TextField(
        help_text="укажите описание", verbose_name="описание курса", **NULLABLE
    )

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
    модель урока
    """

    title = models.CharField(max_length=100, verbose_name="название урока")
    preview = models.ImageField(
        upload_to="materials/preview", verbose_name="превью урока", **NULLABLE
    )
    description = models.TextField(
        help_text="укажите описание", verbose_name="описание урока", **NULLABLE
    )
    lint_to_video = models.TextField(verbose_name="ссылка на видео", **NULLABLE)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, verbose_name="курс", **NULLABLE
    )

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"

    def __str__(self):
        return self.title

class Payment(models.Model):
    payment_choices = (
        ("наличные", "наличные"),
        ("перевод на счет", "перевод на счет")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_day = models.DateField(verbose_name='дата оплаты', auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name='отдельно оплаченный урок', **NULLABLE)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.CharField(max_length=100, choices=payment_choices)
