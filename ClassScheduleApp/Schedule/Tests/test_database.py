from django.test import TestCase

from ..models import *
from datetime import date

# Create your tests here.


class SubjectModelTestCase(TestCase):

    # fixtures = ["group.yaml", "subject.yaml", "users.json", "professor.yaml", "lesson.yaml"]

    fixtures = ['subject.yaml']

    # def setUp(self) -> None:
    #     self.subject = Subject.objects.create(TableName='Филимонов О.Ю.', FullName='Филимонов Олег Юрьевич')
    
    def test_subject_content(self):

        count = Subject.objects.all().count()
        self.assertEqual(count, 7)
    
    def test_concrete_subject(self):

        concreteRecord: Subject = Subject.objects.get(TableName='Схемотехника')

        self.assertEqual(concreteRecord.TableName, 'Схемотехника')
        self.assertEqual(concreteRecord.FullName, '')


class GroupModelTestCase(TestCase):

    # fixtures = ["group.yaml", "subject.yaml", "users.json", "professor.yaml", "lesson.yaml"]

    fixtures = ['group.yaml']
    
    def test_group_content(self):

        count = Group.objects.all().count()
        self.assertEqual(count, 2)
    
    def test_concrete_group(self):

        concreteRecord: Group = Group.objects.get(Name='ИВТ-460')

        self.assertEqual(concreteRecord.Name, 'ИВТ-460')

class LessonModelTestCase(TestCase):

    fixtures = ["group.yaml", "subject.yaml", "users.json", "professor.yaml", "lesson.yaml"]
    
    def test_lesson_content(self):

        count = Lesson.objects.all().count()
        self.assertEqual(count, 18)
    
    def test_lesson_concrete_day(self):

        count = Lesson.objects.filter(Date=date(2019, 10, 26)).all().count()
        self.assertEqual(count, 4)
    
    def test_no_lessons_day(self):

        count = Lesson.objects.filter(Date=date(2020, 10, 26)).all().count()
        self.assertEqual(count, 0)

    def test_group_lessons(self):
        
        group = Group.objects.get(Name='ИВТ-461')
        count = Lesson.objects.filter(Group=group).all().count()
        self.assertEqual(count, 0)


