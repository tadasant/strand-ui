from django.core.management.base import BaseCommand
from app.users.managers import CustomUserManager
from app.users.models import User


class Command(BaseCommand):
    help = 'Adds alias to users'

    def handle(self, *args, **options):
        for user in User.objects.filter(alias__isnull=True):
            user.alias = User.objects.generate_random_alias(4)
            user.save()
