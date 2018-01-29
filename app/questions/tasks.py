from django_celery_beat.models import PeriodicTask, IntervalSchedule


def mark_stale_sessions():
    """
    Task that changes sessions from OPEN to STALE after 30 minutes of inactivity.

    Criteria: Session is marked as OPEN. Last message from non-bot user > 30m ago.
    Action: Change Session status to STALE.
    """
    return None


def close_pending_closed_session(session, datetime_of_last_non_bot_message):
    """
    Task that closes session in PENDING CLOSED after no new activity for 5 additional minutes.

    Criteria: Session is marked as PENDING CLOSED. No new activity.
    Action: Change Session status to CLOSED. Mark Question as SOLVED.
    """
    if datetime_of_last_non_bot_message == session.get_datetime_of_last_non_bot_message():
        session.mark_as_closed()
        session.save()

        session.question.mark_as_solved()
        session.question.save()


schedule, created = IntervalSchedule.objects.get_or_create(
    every=1,
    period=IntervalSchedule.MINUTES
)

PeriodicTask.objects.create(interval=schedule,
                            name='Mark stale sessions',
                            task='app.questions.tasks.mark_stale_sessions')

PeriodicTask.objects.create(interval=schedule,
                            name='Identify sessions to close',
                            task='app.questions.tasks.identify_sessions_to_close')
