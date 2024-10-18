from django.db import models

from config.settings import AUTH_USER_MODEL

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
    update_at = models.DateTimeField(
        verbose_name="дата обновления курса", auto_now_add=True, **NULLABLE
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="создатель курса",
        related_name="courses",
        **NULLABLE
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
    link_to_video = models.TextField(verbose_name="ссылка на видео", **NULLABLE)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, verbose_name="курс", **NULLABLE
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="создатель урока",
        related_name="lessons",
        **NULLABLE
    )

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"

    def __str__(self):
        return self.title
