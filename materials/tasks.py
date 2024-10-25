from datetime import timezone

from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from config import settings
from materials.models import Course
from users.models import Subscription, User


@shared_task
def update_mailing(course_id):
    """
    проводит рассылку подписчикам курса при его обновлении
    """
    subscriptions = Subscription.objects.filter(course=course_id)
    course = get_object_or_404(Course, pk=course_id)
    try:
        send_mail(
            subject="Обновление курса",
            message=f"Курс {course.title} обновлен",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscription.user.email for subscription in subscriptions],
        )
    except Exception as error:
        print(str(error))


@shared_task
def lost_for_us():
    """
    блокирует пользователя если не заходил 30 дней
    """
    today = timezone.now().date()
    users = User.objects.filter(is_active=True, is_staff=False, is_superuser=False)
    for user in users:
        if (timezone.now().date() - user.last_login.date()).days >= 30:
            user.is_active = False
            user.save(update_fields=["is_active"])
