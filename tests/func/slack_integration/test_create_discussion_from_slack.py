import pytest


class TestCreateDiscussionFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_channel_factory, slack_team_factory, discussion_factory,
                             topic_factory):
        topic = topic_factory()
        slack_team = slack_team_factory()
        discussion = discussion_factory.build()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createDiscussionFromSlack(input: {{discussion: {{timeStart: "{discussion.time_start}",
                                                       topicId: {topic.id}}},
                                                       id: "{slack_channel.id}",
                                                       name: "{slack_channel.name}",
                                                       slackTeamId: "{slack_team.id}"}}) {{
              discussion {{
                id
              }}
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createDiscussionFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, auth_client, slack_channel_factory, slack_team_factory, discussion_factory, topic_factory):
        topic = topic_factory()
        slack_team = slack_team_factory()
        discussion = discussion_factory.build()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createDiscussionFromSlack(input: {{discussion: {{timeStart: "{discussion.time_start}",
                                                       topicId: {topic.id}}},
                                                       id: "{slack_channel.id}",
                                                       name: "{slack_channel.name}",
                                                       slackTeamId: "{slack_team.id}"}}) {{
              discussion {{
                topic {{
                  id
                }}
              }}
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createDiscussionFromSlack']['discussion']['topic']['id'] == str(topic.id)
        assert response.json()['data']['createDiscussionFromSlack']['slackChannel']['name'] == slack_channel.name
