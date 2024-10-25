from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course
from users.models import Subscription, User


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Django", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subsription_on(self):
        url = reverse("users:subscribe")
        data = {
            "course": self.course.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subsription_off(self):
        Subscription.objects.create(course=self.course, user=self.user)
        url = reverse("users:subscribe")
        data = {
            "course": self.course.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
