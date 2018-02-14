from app.api.celery import celery_app
from app.topics.models import Discussion, DiscussionStatus
from app.slack_integration.wrappers import SlackAppClientWrapper


@celery_app.task
def mark_stale_discussions():
    """
    Task that changes discussions from OPEN to
    STALE after 30 minutes of inactivity.
    """
    discussions = Discussion.objects.filter(status=DiscussionStatus.OPEN.value).all()
    for discussion in discussions:
        if discussion.minutes_since_last_non_bot_message >= 30.0:
            discussion.mark_as_stale()
            discussion.save()
            if discussion.slack_channel:
                SlackAppClientWrapper.post_stale_discussion(discussion)


@celery_app.task
def auto_close_pending_closed_discussion(discussion_id, datetime_of_last_non_bot_message):
    """
    Task that closes discussion that's been set to PENDING CLOSED
    if there is no new activity for 5 additional minutes.
    """
    discussion = Discussion.objects.get(pk=discussion_id)
    if datetime_of_last_non_bot_message == discussion.datetime_of_last_non_bot_message:
        discussion.mark_as_closed()
        discussion.save()
        if discussion.slack_channel:
            SlackAppClientWrapper.post_auto_closed_discussion(discussion)
