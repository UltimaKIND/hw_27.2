from django.shortcuts import get_object_or_404
from config import settings
from django.core.mail import send_mail
from users.models import Subscription
from celery import shared_task
from materials.models import Course


@shared_task
def update_mailing(course_id):
    subscriptions = Subscription.objects.filter(course=course_id)
    course = get_object_or_404(Course, pk=course_id)
    try:
        send_mail(
            subject='Обновление курса',
            message=f'Курс {course.title} обновлен',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscription.user.email for subscription in subscriptions]
        )
    except Exception as error:
        print(str(error))
