from app.messages.models import Message, Reply

import pytest


class TestCreateSlackTeam:

    @pytest.mark.django_db
    def test_create_slack_team_unauthenticated(self, client, group_factory, slack_team_factory):
        group = group_factory()
        slack_team = slack_team_factory.build()

        mutation = f'''
          mutation {{
            createSlackTeam(input: {{id: "{slack_team.id}", name: "{slack_team.name}", groupId: {group.id}}}) {{
              slackTeam {{
                name
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackTeam'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_slack_team_invalid_group(self, auth_client, slack_team_factory):
        slack_team = slack_team_factory.build()

        mutation = f'''
          mutation {{
            createSlackTeam(input: {{id: "{slack_team.id}", name: "{slack_team.name}", groupId: 1}}) {{
              slackTeam {{
                name
              }}
            }} 
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackTeam'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Group Id'

    @pytest.mark.django_db
    def test_create_slack_team(self, auth_client, group_factory, slack_team_factory):
        group = group_factory()
        slack_team = slack_team_factory.build()

        mutation = f'''
          mutation {{
            createSlackTeam(input: {{id: "{slack_team.id}", name: "{slack_team.name}", groupId: {group.id} }}) {{
              slackTeam {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackTeam']['slackTeam']['name'] == slack_team.name


class TestCreateSlackUser:

    @pytest.mark.django_db
    def test_create_slack_user_unauthenticated(self, client, user_factory, slack_team_factory, slack_user_factory):
        user = user_factory()
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build()

        mutation = f'''
          mutation {{
            createSlackUser(input: {{id: "{slack_user.id}", realName: "{slack_user.real_name}",
                                     displayName: "{slack_user.display_name}", isBot: {str(slack_user.is_bot).lower()},
                                     isAdmin: {str(slack_user.is_admin).lower()}, slackTeamId: "{slack_team.id}",
                                     userId: {user.id}}}) {{
              slackUser {{
                realName
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_slack_user_invalid_team(self, auth_client, user_factory, slack_team_factory, slack_user_factory):
        user = user_factory()
        slack_team = slack_team_factory.build()
        slack_user = slack_user_factory.build()

        mutation = f'''
          mutation {{
            createSlackUser(input: {{id: "{slack_user.id}", realName: "{slack_user.real_name}",
                                     displayName: "{slack_user.display_name}", isBot: {str(slack_user.is_bot).lower()},
                                     isAdmin: {str(slack_user.is_admin).lower()}, slackTeamId: "{slack_team.id}",
                                     userId: {user.id}}}) {{
              slackUser {{
                realName
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['errors'][0]['message'] == 'Invalid Slack Team Id'

    @pytest.mark.django_db
    def test_create_slack_user_invalid_user(self, auth_client, slack_team_factory, slack_user_factory):
        slack_team = slack_team_factory()
        slack_user = slack_user_factory()

        mutation = f'''
          mutation {{
            createSlackUser(input: {{id: "{slack_user.id}", realName: "{slack_user.real_name}",
                                     displayName: "{slack_user.display_name}", isBot: {str(slack_user.is_bot).lower()},
                                     isAdmin: {str(slack_user.is_admin).lower()}, slackTeamId: "{slack_team.id}",
                                     userId: 1}}) {{
              slackUser {{
                realName
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['errors'][0]['message'] == 'Invalid User Id'

    @pytest.mark.django_db
    def test_create_slack_user(self, auth_client, user_factory, slack_team_factory, slack_user_factory):
        user = user_factory()
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build()

        mutation = f'''
          mutation {{
            createSlackUser(input: {{id: "{slack_user.id}", realName: "{slack_user.real_name}",
                                     displayName: "{slack_user.display_name}", isBot: {str(slack_user.is_bot).lower()},
                                     isAdmin: {str(slack_user.is_admin).lower()}, slackTeamId: "{slack_team.id}",
                                     userId: {user.id}}}) {{
              slackUser {{
                realName
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackUser']['slackUser']['realName'] == slack_user.real_name


class TestCreateSlackChannel:

    @pytest.mark.django_db
    def test_create_slack_channel_unauthenticated(self, client, slack_channel_factory, slack_team_factory, session_factory):
        session = session_factory()
        slack_team = slack_team_factory()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createSlackChannel(input: {{id: "{slack_channel.id}", name: "{slack_channel.name}",
                                        slackTeamId: "{slack_team.id}", sessionId: {session.id}}}) {{
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_slack_channel_invalid_team(self, auth_client, slack_channel_factory, slack_team_factory, session_factory):
        session = session_factory()
        slack_team = slack_team_factory.build()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createSlackChannel(input: {{id: "{slack_channel.id}", name: "{slack_channel.name}",
                                        slackTeamId: "{slack_team.id}", sessionId: {session.id}}}) {{
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Slack Team Id'

    @pytest.mark.django_db
    def test_create_slack_channel_invalid_session(self, auth_client, slack_channel_factory, slack_team_factory):
        slack_team = slack_team_factory()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createSlackChannel(input: {{id: "{slack_channel.id}", name: "{slack_channel.name}",
                                        slackTeamId: "{slack_team.id}", sessionId: 0}}) {{
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Session Id'

    @pytest.mark.django_db
    def test_create_slack_channel(self, auth_client, slack_channel_factory, slack_team_factory, session_factory):
        session = session_factory()
        slack_team = slack_team_factory()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createSlackChannel(input: {{id: "{slack_channel.id}", name: "{slack_channel.name}",
                                        slackTeamId: "{slack_team.id}", sessionId: {session.id}}}) {{
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel']['slackChannel']['name'] == slack_channel.name


class TestCreateSessionAndSlackChannel:

    @pytest.mark.django_db
    def test_create_session_and_slack_channel_unauthenticated(self, client, slack_channel_factory, slack_team_factory,
                                                              session_factory, question_factory):
        question = question_factory()
        slack_team = slack_team_factory()
        session = session_factory.build()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createSessionAndSlackChannel(input: {{session: {{timeStart: "{session.time_start}",
                                                             questionId: {question.id}}},
                                                  id: "{slack_channel.id}",
                                                  name: "{slack_channel.name}",
                                                  slackTeamId: "{slack_team.id}"}}) {{
              session {{
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
        assert response.json()['data']['createSessionAndSlackChannel'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_session_and_slack_channel(self, auth_client, slack_channel_factory, slack_team_factory,
                                              session_factory, question_factory):
        question = question_factory()
        slack_team = slack_team_factory()
        session = session_factory.build()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createSessionAndSlackChannel(input: {{session: {{timeStart: "{session.time_start}",
                                                             questionId: {question.id}}},
                                                  id: "{slack_channel.id}",
                                                  name: "{slack_channel.name}",
                                                  slackTeamId: "{slack_team.id}"}}) {{
              session {{
                question {{
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
        assert response.json()['data']['createSessionAndSlackChannel']['session']['question']['id'] == str(question.id)
        assert response.json()['data']['createSessionAndSlackChannel']['slackChannel']['name'] == slack_channel.name


class TestCreateSlackSettings:

    @pytest.mark.django_db
    def test_create_slack_settings_unauthenticated(self, client, slack_team_factory):
        slack_team = slack_team_factory()

        mutation = f'''
          mutation {{
            createSlackSettings(input: {{botToken: "123AAA", slackTeamId: "{slack_team.id}"}}) {{
              slackSettings {{
                botToken
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackSettings'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_slack_settings_invalid_team(self, auth_client):
        mutation = f'''
          mutation {{
            createSlackSettings(input: {{botToken: "123AAA", slackTeamId: "123AAA"}}) {{
              slackSettings {{
                botToken
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackSettings'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Slack Team Id'

    @pytest.mark.django_db
    def test_create_slack_settings(self, auth_client, slack_team_factory):
        slack_team = slack_team_factory()

        mutation = f'''
          mutation {{
            createSlackSettings(input: {{botToken: "123AAA", slackTeamId: "{slack_team.id}"}}) {{
              slackSettings {{
                botToken
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackSettings']['slackSettings']['botToken'] == '123AAA'


class TestCreateSlackEventAndMessage:
    @pytest.mark.django_db
    def test_create_slack_event_and_message_unauthenticated(self, client, session_factory, user_factory,
                                                            slack_event_factory, message_factory):
        session = session_factory()
        user = user_factory()
        slack_event = slack_event_factory.build()
        message = message_factory.build(session=session, author=user)

        mutation = f'''
          mutation {{
            createSlackEventAndMessage(input: {{text: "{message.text}", sessionId: {session.id}, authorId: {user.id},
                                                time: "{message.time}",
                                                slackEventTs: "{slack_event.ts}"}}) {{
              message {{
                text
              }}
            }}
          }}        
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackEventAndMessage'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_slack_event_and_message(self, auth_client, session_factory, user_factory, slack_event_factory,
                                            message_factory):
        session = session_factory()
        user = user_factory()
        slack_event = slack_event_factory.build()
        message = message_factory.build(session=session, author=user)

        mutation = f'''
          mutation {{
            createSlackEventAndMessage(input: {{text: "{message.text}", sessionId: {session.id}, authorId: {user.id},
                                                time: "{message.time}", slackEventTs: "{slack_event.ts}"}}) {{
              message {{
                id
                text
              }}
            }}
          }}        
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackEventAndMessage']['message']['text'] == message.text

        new_message_id = response.json()['data']['createSlackEventAndMessage']['message']['id']
        assert Message.objects.get(pk=new_message_id).slack_event_id


class TestCreateSlackEventAndReply:

    @pytest.mark.django_db
    def test_create_slack_event_and_reply_unauthenticated(self, client, message_factory, user_factory,
                                                          slack_event_factory, reply_factory):
        message = message_factory()
        user = user_factory()
        slack_event = slack_event_factory.build()
        reply = reply_factory.build(message=message, author=user)

        mutation = f'''
          mutation {{
            createSlackEventAndReply(input: {{text: "{reply.text}", messageId: {message.id}, authorId: {user.id},
                                              time: "{reply.time}", slackEventTs: "{slack_event.ts}"}}) {{
              reply {{
                text
              }}
            }}
          }}        
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackEventAndReply'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_slack_event_and_reply(self, auth_client, message_factory, user_factory,
                                          slack_event_factory, reply_factory):
        message = message_factory()
        user = user_factory()
        slack_event = slack_event_factory.build()
        reply = reply_factory.build(message=message, author=user)

        mutation = f'''
          mutation {{
            createSlackEventAndReply(input: {{text: "{reply.text}", messageId: {message.id}, authorId: {user.id},
                                              time: "{reply.time}", slackEventTs: "{slack_event.ts}"}}) {{
              reply {{
                id
                text
              }}
            }}
          }}        
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackEventAndReply']['reply']['text'] == reply.text

        new_reply_id = response.json()['data']['createSlackEventAndReply']['reply']['id']
        assert Reply.objects.get(pk=new_reply_id).slack_event_id

