from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    help = 'Creates periodic tasks'

    def handle(self, *args, **options):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS,
        )

        PeriodicTask.objects.create(
            interval=schedule,
            name='Mark stale sessions',
            task='app.questions.tasks.mark_stale_sessions'
        )
