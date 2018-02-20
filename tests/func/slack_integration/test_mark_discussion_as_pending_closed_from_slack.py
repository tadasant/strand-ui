import pytest


class TestMarkDiscussionAsPendingClosedFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, topic_factory, discussion_factory, slack_channel_factory):
        topic = topic_factory()
        discussion = discussion_factory(topic=topic, status='STALE')
        slack_channel = slack_channel_factory(discussion=discussion)

        mutation = f'''
          mutation {{
            markDiscussionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              discussion {{
                status
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})
        assert response.status_code == 200
        assert response.json()['data']['markDiscussionAsPendingClosedFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, topic_factory, discussion_factory, slack_channel_factory):
        topic = topic_factory()
        discussion = discussion_factory(topic=topic, status='STALE')
        slack_channel = slack_channel_factory.build(discussion=discussion)

        mutation = f'''
          mutation {{
            markDiscussionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              discussion {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['markDiscussionAsPendingClosedFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Discussion matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_discussion_state(self, auth_client, topic_factory, discussion_factory, slack_channel_factory):
        topic = topic_factory()
        discussion = discussion_factory(topic=topic, status='OPEN')
        slack_channel = slack_channel_factory(discussion=discussion)

        mutation = f'''
          mutation {{
            markDiscussionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              discussion {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['markDiscussionAsPendingClosedFromSlack'] is None
        assert response.json()['errors'][0]['message'] == "Can't switch from state 'OPEN' using method " \
                                                          "'mark_as_pending_closed'"

    @pytest.mark.django_db
    def test_valid(self, auth_client, topic_factory, discussion_factory, slack_channel_factory,
                   auto_close_pending_closed_discussion_factory, slack_app_request_factory):
        topic = topic_factory()
        discussion = discussion_factory(topic=topic, status='STALE')
        slack_channel = slack_channel_factory(discussion=discussion)

        mutation = f'''
          mutation {{
            markDiscussionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              discussion {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['markDiscussionAsPendingClosedFromSlack']['discussion'][
                   'status'] == 'PENDING CLOSED'
