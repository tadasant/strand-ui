from app.api.celery import celery_app
from app.questions.models import Session, SessionStatus


@celery_app.task
def mark_stale_sessions():
    """
    Task that changes sessions from OPEN to
    STALE after 30 minutes of inactivity.
    """
    sessions = Session.objects.filter(status=SessionStatus.OPEN.value).all()
    for session in sessions:
        if session.minutes_since_last_non_bot_message >= 30.0:
            session.mark_as_stale()
            session.save()


@celery_app.task
def auto_close_pending_closed_session(session_id, datetime_of_last_non_bot_message):
    """
    Task that closes session that's been set to PENDING CLOSED
    if there is no new activity for 5 additional minutes.
    """
    session = Session.objects.get(pk=session_id)
    if datetime_of_last_non_bot_message == session.datetime_of_last_non_bot_message:
        session.mark_as_closed()
        session.save()

        session.question.mark_as_solved()
        session.question.save()
