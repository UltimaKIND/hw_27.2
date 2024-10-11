# Generated by Django 5.1.1 on 2024-10-11 14:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0002_course_owner_lesson_owner"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="payment",
            options={
                "ordering": ("payment_date",),
                "verbose_name": "Платеж",
                "verbose_name_plural": "Платежи",
            },
        ),
        migrations.RenameField(
            model_name="payment",
            old_name="payment_day",
            new_name="payment_date",
        ),
        migrations.RemoveField(
            model_name="payment",
            name="payment",
        ),
        migrations.RemoveField(
            model_name="payment",
            name="payment_amount",
        ),
        migrations.AddField(
            model_name="payment",
            name="link",
            field=models.URLField(
                blank=True,
                help_text="Укажите ссылку на оплату",
                max_length=400,
                null=True,
                verbose_name="ссылка на оплату",
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="session_id",
            field=models.CharField(
                blank=True,
                help_text="Укажите Id сессии",
                max_length=255,
                null=True,
                verbose_name="Id сессии",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="materials.course",
                        verbose_name="курс подписки",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="подписка пользователя",
                    ),
                ),
            ],
        ),
    ]