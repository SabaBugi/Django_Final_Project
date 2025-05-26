from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Creates 10 new users'

    def handle(self, *args, **kwargs):
        for i in range(1, 11):
            email = f'user{i}@example.com'
            if not CustomUser.objects.filter(email=email).exists():
                CustomUser.objects.create_user(
                    email=email,
                    password='TestPassword123',
                    first_name=f'User{i}',
                    last_name='Test'
                )
                self.stdout.write(self.style.SUCCESS(f'Created user: {email}'))
            else:
                self.stdout.write(self.style.WARNING(f'User already exists: {email}'))