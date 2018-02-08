from django.conf import settings
import requests

from app.api.celery import celery_app
from app.topics.models import Discussion, DiscussionStatus


def post_discussion_to_slack_app(endpoint, discussion):
    payload = {'discussion_id': discussion.id, 'slack_channel_id': discussion.slack_channel.id,
               'status': discussion.status}
    requests.post(endpoint, data=payload, headers={'Authorization': f'Token {settings.SLACK_APP_VERIFICATION_TOKEN}'})


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
            post_discussion_to_slack_app(settings.SLACK_APP_STALE_DISCUSSION_ENDPOINT, discussion)


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
        post_discussion_to_slack_app(settings.SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT, discussion)

