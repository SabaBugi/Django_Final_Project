from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from tasks.models import Task

class Command(BaseCommand):
    help = 'Send notifications for tasks due in 1 day'

    def handle(self, *args, **kwargs):
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        tasks = Task.objects.filter(due_date=tomorrow)
        for task in tasks:
            if task.user and task.user.email:
                send_mail(
                    subject='Task Due Soon',
                    message=f'Your task "{task.title}" is due tomorrow ({task.due_date}, {task.time}).',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[task.user.email],
                    fail_silently=True,
                )
                self.stdout.write(self.style.SUCCESS(f'Notification sent for task: {task.title}'))