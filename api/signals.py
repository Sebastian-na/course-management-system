from .models import User, Professor, Student
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user(sender, instance: User, created, **kwargs):
    if created:
        if instance.user_type == User.PROFESSOR:
            Professor.objects.create(user=instance)
        elif instance.user_type == User.STUDENT:
            Student.objects.create(user=instance)
