import pytest


class TestCloseDiscussionFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, discussion_factory, slack_channel_factory):
        discussion = discussion_factory()
        slack_channel = slack_channel_factory(discussion=discussion)
        time_end = discussion_factory.build().time_end

        mutation = f'''
          mutation {{
            closeDiscussionFromSlack(input: {{slackChannelId: "{slack_channel.id}",
                                            timeEnd: "{time_end}"}}) {{
              discussion {{
                id
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['closeDiscussionFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, discussion_factory, slack_channel_factory):
        discussion = discussion_factory()
        slack_channel = slack_channel_factory.build(discussion=discussion)
        time_end = discussion_factory.build().time_end

        mutation = f'''
          mutation {{
            closeDiscussionFromSlack(input: {{slackChannelId: "{slack_channel.id}",
                                            timeEnd: "{time_end}"}}) {{
              discussion {{
                id
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['closeDiscussionFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Discussion matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, discussion_factory, slack_channel_factory):
        discussion = discussion_factory()
        slack_channel = slack_channel_factory(discussion=discussion)
        time_end = discussion_factory.build().time_end

        mutation = f'''
          mutation {{
            closeDiscussionFromSlack(input: {{slackChannelId: "{slack_channel.id}",
                                            timeEnd: "{time_end}"}}) {{
              discussion {{
                id
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['closeDiscussionFromSlack']['discussion']['id'] == str(discussion.id)
