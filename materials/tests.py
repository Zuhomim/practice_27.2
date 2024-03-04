from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from materials.models import Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.user = User.objects.create(email='admin@gmail.com', is_superuser=True, is_staff=True)
        self.client.force_authenticate(user=self.user)

        self.lesson = Lesson.objects.create(
            name='Test',
            description='Test_lesson',
            video_link='https://www.youtube.com/1',
            owner=self.user,
        )
        self.user.set_password("password")
        self.user.save()

    def test_create_lesson(self):

        data = {
            "name": "test",
            "description": "test",
        }
        response = self.client.post(
            reverse('materials:lesson_create'),
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_retrieve_lesson(self):

        response = self.client.get(
            reverse('materials:lesson_retrieve', args=[self.lesson.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.lesson.name)

    def test_lesson_list(self):

        response = self.client.get(
            reverse('materials:lesson_list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['results'][0].name, self.lesson.name)

    def test_update_lesson(self):

        update_data = {
            "description": "updated"
        }
        response = self.client.patch(
            reverse('materials:lesson_update', args=[self.lesson.id]), update_data
        )
        self.lesson.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], update_data['description'])

    def test_delete_lesson(self):

        response = self.client.delete(
            reverse('materials:lesson_delete', args=[self.lesson.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_lesson_validation_error(self):

        data = {
            "name": "Test",
            "description": "test",
            "video_link": "https://www.rutube.com/watch?v=i-uvtDKeFgE&list=PLA0M1Bcd0w8xZA3Kl1fYmOH_MfLpiYMRs",
        }
        response = self.client.post(
            reverse('materials:lesson_create'),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ["Запрещено использовать сторонние ссылки"]})
