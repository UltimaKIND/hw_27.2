from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Django", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="first_lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("materials:course-detail", args=[self.course.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("lessons_count"), 1)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_create(self):
        url = reverse("materials:course-list")
        data = {
            "title": "DRF",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("materials:course-detail", args=[self.course.pk])
        data = {"title": "Java"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Java")

    def test_course_delete(self):
        url = reverse("materials:course-detail", args=[self.course.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "title": self.course.title,
                    "preview": self.course.preview,
                    "description": self.course.description,
                    "owner": self.user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Django", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="first_lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson_detail", args=[self.lesson.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")
        data = {"title": "test_lesson", "course": self.course.pk, "owner": self.user.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("materials:lesson_update", args=[self.lesson.pk])
        data = {"title": "second_lesson"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "second_lesson")

    def test_lesson_delete(self):
        url = reverse("materials:lesson_delete", args=[self.lesson.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "preview": self.lesson.preview,
                    "description": self.lesson.description,
                    "link_to_video": self.lesson.link_to_video,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
