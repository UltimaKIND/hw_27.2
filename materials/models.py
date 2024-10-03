from django.db import models

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
