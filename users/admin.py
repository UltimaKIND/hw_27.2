from django.contrib import admin

from users.models import Payment, User


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "payment_date",
        "course",
        "lesson",
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")
