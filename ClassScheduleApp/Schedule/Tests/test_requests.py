from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from ..models import *
from datetime import date

# Create your tests here.


class SubjectRequestsTestCase(APITestCase):

    fixtures = ['subject.yaml']

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient(enforce_csrf_checks=True)
        cls.url_subject_exists_id = reverse('SubjectId', args=[1])
        cls.url_subject_not_exists_id = reverse('SubjectId', args=[10])
        cls.url_subjects = reverse('Subjects')

    def test_subject_id(self):

        response = self.client.get(self.url_subject_exists_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subject'], 'Задачи математической физики')
    
    def test_subject_not_exists(self):

        response = self.client.get(self.url_subject_not_exists_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    
    def test_subjects(self):

        response = self.client.get(self.url_subjects)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['subjects']), 7)


class LessonRequestsTestCase(APITestCase):

    fixtures = ["group.yaml", "subject.yaml", "users.json", "professor.yaml", "lesson.yaml"]

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient(enforce_csrf_checks=True)
        cls.url_lesson_non_date = reverse('LessonYMDView', args=[10, 10, 10]) + '?group=ИВТ-460'
        cls.url_lesson_date= reverse('LessonYMDView', args=[2019, 10, 26]) + '?group=ИВТ-460'
        cls.url_lesson_id = reverse('LessonIdView', args=[1])
        cls.url_lesson_non_id = reverse('LessonIdView', args=[100])

    def test_lesson_id(self):

        response = self.client.get(self.url_lesson_id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['classroom'], 'В802')

    def test_lesson_non_id(self):

        response = self.client.get(self.url_lesson_non_id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_lesson_date(self):

        response = self.client.get(self.url_lesson_date)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_non_date(self):

        response = self.client.get(self.url_lesson_non_date)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['lessons'], [])
