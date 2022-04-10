from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Group(models.Model):
    Name = models.CharField(max_length=255, db_column='Name', unique=True)


class Subject(models.Model):
    TableName = models.CharField(max_length=255, db_column='TableName')
    FullName = models.CharField(max_length=255, db_column='FullName')


class Lesson(models.Model):
    Classroom = models.CharField(max_length=255, db_column='Classroom')
    Date = models.DateField(db_column='Date')
    Time = models.CharField(max_length=255, db_column='Time')

    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE, db_column='SubjectId')
    Professor = models.ForeignKey(User, on_delete=models.CASCADE, db_column='ProfessorId')
    Group = models.ForeignKey(Group, on_delete=models.CASCADE, db_column='GroupId')

    @staticmethod
    def GetCampus():
        return Lesson.objects.values_list('Campus')

    @staticmethod
    def GetClassroom():
        return Lesson.objects.values_list('Classroom')