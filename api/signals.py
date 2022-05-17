from .models import User, Professor, Student
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user(sender, instance: User, created, **kwargs):
    if created:
        if instance.user_type == User.PROFESSOR:
            Professor.objects.create(user=instance)
        elif instance.user_type == User.STUDENT:
            Student.objects.create(user=instance)

@receiver(post_delete, sender=Student)
def delete_student(sender, instance: Student, **kwargs):
    instance.user.delete()

@receiver(post_delete, sender=Professor)
def delete_professor(sender, instance: Professor, **kwargs):
    instance.user.delete()
