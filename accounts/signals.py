from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from tasks.models import Project

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='Welcome to Task Manager!',
            message='Hello {},\n\nThank you for registering at Task Manager!'.format(
                instance.first_name or instance.email
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=True,
        )

@receiver(post_save, sender=Project)
def notify_project_created(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='New Project Created',
            message='Your project "{}" has been created successfully!'.format(instance.name),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.owner.email],
            fail_silently=True,
        )