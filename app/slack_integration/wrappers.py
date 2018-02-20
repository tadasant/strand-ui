import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


class SlackAppClientWrapper:
    @staticmethod
    def _construct_headers():
        headers = {'Authorization': f'Token {settings.SLACK_APP_VERIFICATION_TOKEN}',
                   'Content-Type': 'application/json'}
        return headers

    @staticmethod
    def _construct_discussion_payload(discussion):
        return {'slack_channel_id': discussion.slack_channel.id,
                'slack_team_id': discussion.slack_channel.slack_team.id}

    @staticmethod
    def _construct_slack_agent_payload(slack_agent):
        slack_agent_payload = {'status': slack_agent.status,
                               'topic_channel_id': slack_agent.topic_channel_id,
                               'slack_application_installation': {},
                               'slack_team': {}}
        try:
            slack_team = slack_agent.slack_team
            slack_agent_payload['slack_team'] = {'id': slack_team.id}
        except ObjectDoesNotExist:
            pass

        try:
            slack_application_installation = slack_agent.slack_application_installation
            slack_agent_payload['slack_application_installation'] = {
                'access_token': slack_application_installation.access_token,
                'bot_access_token': slack_application_installation.bot_access_token,
                'bot_user_id': slack_application_installation.bot_user_id,
                'installer': {
                    'id': slack_application_installation.installer.id,
                    'name': slack_application_installation.installer.name,
                    'real_name': slack_application_installation.installer.real_name,
                    'is_bot': slack_application_installation.installer.is_bot,
                    'is_admin': slack_application_installation.installer.is_admin,
                    'team_id': slack_application_installation.installer.slack_team_id,
                    'profile': {
                        'image_72': slack_application_installation.installer.image_72,
                        'first_name': slack_application_installation.installer.first_name,
                        'last_name': slack_application_installation.installer.last_name,
                        'display_name': slack_application_installation.installer.display_name,
                        'email': slack_application_installation.installer.email
                    }
                }
            }
        except ObjectDoesNotExist:
            pass

        return slack_agent_payload

    @staticmethod
    def _post_discussion(endpoint, discussion):
        headers = SlackAppClientWrapper._construct_headers()
        payload = SlackAppClientWrapper._construct_discussion_payload(discussion)

        resp = requests.post(endpoint, json=payload, headers=headers)
        assert resp.status_code == 200, resp.content

    @staticmethod
    def post_auto_closed_discussion(discussion):
        SlackAppClientWrapper._post_discussion(settings.SLACK_APP_AUTO_CLOSED_DISCUSSION_ENDPOINT,
                                               discussion)

    @staticmethod
    def post_stale_discussion(discussion):
        SlackAppClientWrapper._post_discussion(settings.SLACK_APP_STALE_DISCUSSION_ENDPOINT,
                                               discussion)

    @staticmethod
    def post_slack_agent(slack_agent):
        headers = SlackAppClientWrapper._construct_headers()
        payload = SlackAppClientWrapper._construct_slack_agent_payload(slack_agent)

        resp = requests.post(settings.SLACK_APP_SLACK_AGENT_ENDPOINT, json=payload, headers=headers)
        assert resp.status_code == 200, resp.content

    @staticmethod
    def put_slack_agent(slack_agent):
        headers = SlackAppClientWrapper._construct_headers()
        payload = SlackAppClientWrapper._construct_slack_agent_payload(slack_agent)

        resp = requests.put(settings.SLACK_APP_SLACK_AGENT_ENDPOINT, json=payload, headers=headers)
        assert resp.status_code == 200, resp.content
