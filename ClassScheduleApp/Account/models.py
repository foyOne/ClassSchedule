from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Professor(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    TableName = models.CharField(max_length=255, db_column='TableName')


@receiver(post_save, sender=User)
def create_professor_for_user(sender, instance, created, **kwargs):
    if created:
        Professor.objects.create(User=instance)

@receiver(post_save, sender=User)
def save_professor_profile(sender, instance, **kwargs):
    instance.professor.save()


