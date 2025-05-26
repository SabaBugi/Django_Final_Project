from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Task)
def task_created_signal(sender, instance, created, **kwargs):
    if created:
        # Example: send an email to the task owner
        send_mail(
            subject='New Task Created',
            message=f'Your task "{instance.title}" has been created.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email],
            fail_silently=True,
        )