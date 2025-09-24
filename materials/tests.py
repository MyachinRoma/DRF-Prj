import os
import django
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # <-- укажи свой модуль настроек
django.setup()


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.course = Course.objects.create(
            title="test_course", description="test_description"
        )
        self.lesson = Lesson.objects.create(
            title="test_lesson", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        url = reverse("materials:lessons_create")
        data = {
            "title": "test_lesson",
            "description": "test_description",
            "course": self.course.pk,
            "video_url": "http://youtube.com/",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {
            "title": "test_lesson",
            "description": "test_description",
            "course": self.course.pk,
            "link_to_video": "http://youtube.com/",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "test_description")

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lessons_list")
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
                    "course": self.course.pk,
                    "owner": self.user.pk,
                    "video_url": self.lesson.video_url,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(
            title="test_course",
            description="test_description",
            owner=self.user,
        )

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:subscribe")
        response = self.client.post(url, {"course_id": self.course.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Подписка добавлена.")
        self.assertTrue(
            Subscription.objects.filter
            (user=self.user, course=self.course).exists()
        )

    def test_unsubscribe_from_course(self):
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        url = reverse("materials:subscribe")
        response = self.client.post(url, {"course_id": self.course.pk})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Подписка удалена.")
        self.assertFalse(
            Subscription.objects.filter
            (user=self.user, course=self.course).exists()
        )

    def test_subscribe_to_nonexistent_course(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:subscribe")
        response = self.client.post(url, {"course_id": 1000})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_user(self):
        url = reverse("materials:subscribe")
        response = self.client.post(url, {"course_id": self.course.pk})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
