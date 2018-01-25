import pytest


class TestCreateUserAndMessageFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, message_factory, slack_event_factory, slack_user_factory,
                             slack_channel_factory, slack_team_factory):
        slack_team = slack_team_factory()
        slack_event = slack_event_factory.build()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        message = message_factory.build()
        slack_channel = slack_channel_factory()

        mutation = f'''
          mutation {{
            createUserAndMessageFromSlack(input: {{slackUser: {{id: "{slack_user.id}",
                                                                name: "{slack_user.name}",
                                                                firstName: "{slack_user.first_name}",
                                                                lastName: "{slack_user.last_name}",
                                                                realName: "{slack_user.real_name}",
                                                                displayName: "{slack_user.display_name}",
                                                                email: "{slack_user.email}",
                                                                avatar72: "{slack_user.avatar_72}",
                                                                isBot: {str(slack_user.is_bot).lower()},
                                                                isAdmin: {str(slack_user.is_admin).lower()},
                                                                slackTeamId: "{slack_user.slack_team_id}"}},
                                                    originSlackEventTs: "{slack_event.ts}",
                                                    slackChannelId: "{slack_channel.id}",
                                                    text: "{message.text}"}}) {{
              slackUser {{
                user {{
                  firstName
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})
        print(response.content)
        assert response.status_code == 200
        assert response.json()['data']['createUserAndMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_user(self, auth_client, message_factory, slack_event_factory, slack_user_factory,
                                slack_channel_factory, slack_team_factory):
        slack_team = slack_team_factory()
        slack_event = slack_event_factory.build()
        slack_user = slack_user_factory(slack_team=slack_team)
        message = message_factory.build()
        slack_channel = slack_channel_factory()

        mutation = f'''
          mutation {{
            createUserAndMessageFromSlack(input: {{slackUser: {{id: "{slack_user.id}",
                                                                name: "{slack_user.name}",
                                                                firstName: "{slack_user.first_name}",
                                                                lastName: "{slack_user.last_name}",
                                                                realName: "{slack_user.real_name}",
                                                                displayName: "{slack_user.display_name}",
                                                                email: "{slack_user.email}",
                                                                avatar72: "{slack_user.avatar_72}",
                                                                isBot: {str(slack_user.is_bot).lower()},
                                                                isAdmin: {str(slack_user.is_admin).lower()},
                                                                slackTeamId: "{slack_user.slack_team_id}"}},
                                                    originSlackEventTs: "{slack_event.ts}",
                                                    slackChannelId: "{slack_channel.id}",
                                                    text: "{message.text}"}}) {{
              slackUser {{
                user {{
                  firstName
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == "{'id': ['slack user with this id already exists.']}"

    @pytest.mark.django_db
    def test_invalid_slack_team(self, auth_client, message_factory, slack_event_factory, slack_user_factory,
                                slack_channel_factory):
        slack_event = slack_event_factory.build()
        slack_user = slack_user_factory.build()
        message = message_factory.build()
        slack_channel = slack_channel_factory()

        mutation = f'''
          mutation {{
            createUserAndMessageFromSlack(input: {{slackUser: {{id: "{slack_user.id}",
                                                                name: "{slack_user.name}",
                                                                firstName: "{slack_user.first_name}",
                                                                lastName: "{slack_user.last_name}",
                                                                realName: "{slack_user.real_name}",
                                                                displayName: "{slack_user.display_name}",
                                                                email: "{slack_user.email}",
                                                                avatar72: "{slack_user.avatar_72}",
                                                                isBot: {str(slack_user.is_bot).lower()},
                                                                isAdmin: {str(slack_user.is_admin).lower()},
                                                                slackTeamId: "{slack_user.slack_team_id}"}},
                                                    originSlackEventTs: "{slack_event.ts}",
                                                    slackChannelId: "{slack_channel.id}",
                                                    text: "{message.text}"}}) {{
              slackUser {{
                user {{
                  firstName
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == f"{{'slack_team_id': ['Invalid pk " \
                                                          f"\"{slack_user.slack_team_id}\" - " \
                                                          "object does not exist.']}"

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, message_factory, slack_event_factory, slack_user_factory,
                                   slack_channel_factory, slack_team_factory):
        slack_team = slack_team_factory()
        slack_event = slack_event_factory.build()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        message = message_factory.build()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createUserAndMessageFromSlack(input: {{slackUser: {{id: "{slack_user.id}",
                                                                name: "{slack_user.name}",
                                                                firstName: "{slack_user.first_name}",
                                                                lastName: "{slack_user.last_name}",
                                                                realName: "{slack_user.real_name}",
                                                                displayName: "{slack_user.display_name}",
                                                                email: "{slack_user.email}",
                                                                avatar72: "{slack_user.avatar_72}",
                                                                isBot: {str(slack_user.is_bot).lower()},
                                                                isAdmin: {str(slack_user.is_admin).lower()},
                                                                slackTeamId: "{slack_user.slack_team_id}"}},
                                                    originSlackEventTs: "{slack_event.ts}",
                                                    slackChannelId: "{slack_channel.id}",
                                                    text: "{message.text}"}}) {{
              slackUser {{
                user {{
                  firstName
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Session matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, message_factory, slack_event_factory, slack_user_factory,
                   slack_channel_factory, slack_team_factory):
        slack_team = slack_team_factory()
        slack_event = slack_event_factory.build()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        message = message_factory.build()
        slack_channel = slack_channel_factory()

        mutation = f'''
          mutation {{
            createUserAndMessageFromSlack(input: {{slackUser: {{id: "{slack_user.id}",
                                                                name: "{slack_user.name}",
                                                                firstName: "{slack_user.first_name}",
                                                                lastName: "{slack_user.last_name}",
                                                                realName: "{slack_user.real_name}",
                                                                displayName: "{slack_user.display_name}",
                                                                email: "{slack_user.email}",
                                                                avatar72: "{slack_user.avatar_72}",
                                                                isBot: {str(slack_user.is_bot).lower()},
                                                                isAdmin: {str(slack_user.is_admin).lower()},
                                                                slackTeamId: "{slack_user.slack_team_id}"}},
                                                    originSlackEventTs: "{slack_event.ts}",
                                                    slackChannelId: "{slack_channel.id}",
                                                    text: "{message.text}"}}) {{
              slackUser {{
                user {{
                  firstName
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndMessageFromSlack']['slackUser']['user']['firstName'] == \
            slack_user.first_name
