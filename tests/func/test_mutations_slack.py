import pytest


class TestCreateSlackTeam:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, group_factory, slack_team_factory):
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
    def test_invalid_group(self, auth_client, slack_team_factory):
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
    def test_valid(self, auth_client, group_factory, slack_team_factory):
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
    def test_unauthenticated(self, client, user_factory, slack_team_factory, slack_user_factory):
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
    def test_invalid_team(self, auth_client, user_factory, slack_team_factory, slack_user_factory):
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
    def test_invalid_user(self, auth_client, slack_team_factory, slack_user_factory):
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
    def test_valid(self, auth_client, user_factory, slack_team_factory, slack_user_factory):
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
    def test_unauthenticated(self, client, slack_channel_factory, slack_team_factory, session_factory):
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
    def test_invalid_team(self, auth_client, slack_channel_factory, slack_team_factory, session_factory):
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
    def test_invalid_session(self, auth_client, slack_channel_factory, slack_team_factory):
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
    def test_valid(self, auth_client, slack_channel_factory, slack_team_factory, session_factory):
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


class TestCreateSessionFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_channel_factory, slack_team_factory, session_factory,
                             question_factory):
        question = question_factory()
        slack_team = slack_team_factory()
        session = session_factory.build()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createSessionFromSlack(input: {{session: {{timeStart: "{session.time_start}",
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
        assert response.json()['data']['createSessionFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, auth_client, slack_channel_factory, slack_team_factory, session_factory, question_factory):
        question = question_factory()
        slack_team = slack_team_factory()
        session = session_factory.build()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createSessionFromSlack(input: {{session: {{timeStart: "{session.time_start}",
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
        assert response.json()['data']['createSessionFromSlack']['session']['question']['id'] == str(question.id)
        assert response.json()['data']['createSessionFromSlack']['slackChannel']['name'] == slack_channel.name


class TestCreateSlackTeamSetting:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_team_factory, slack_team_setting_factory):
        slack_team = slack_team_factory()
        slack_team_setting = slack_team_setting_factory.build(slack_team=slack_team)

        mutation = f'''
          mutation {{
            createSlackTeamSetting(input: {{slackTeamId: "{slack_team.id}", name: "{slack_team_setting.name}",
                                            value: "{slack_team_setting.value}",
                                            dataType: "{slack_team_setting.data_type}"}}) {{
              slackTeamSetting {{
                name
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackTeamSetting'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_team(self, auth_client, slack_team_setting_factory):
        slack_team_setting = slack_team_setting_factory.build()

        mutation = f'''
          mutation {{
            createSlackTeamSetting(input: {{slackTeamId: "123AAA", name: "{slack_team_setting.name}",
                                            value: "{slack_team_setting.value}",
                                            dataType: "{slack_team_setting.data_type}"}}) {{
              slackTeamSetting {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackTeamSetting'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Slack Team Id'

    @pytest.mark.django_db
    def test_valid(self, auth_client, slack_team_factory, slack_team_setting_factory):
        slack_team = slack_team_factory()
        slack_team_setting = slack_team_setting_factory.build(slack_team=slack_team)

        mutation = f'''
          mutation {{
            createSlackTeamSetting(input: {{slackTeamId: "{slack_team.id}", name: "{slack_team_setting.name}",
                                            value: "{slack_team_setting.value}",
                                            dataType: "{slack_team_setting.data_type}"}}) {{
              slackTeamSetting {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackTeamSetting']['slackTeamSetting']['name'] == slack_team_setting.name


class TestCreateSlackTeamInstallation:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_team_factory, slack_user_factory,
                             slack_team_installation_factory):
        slack_team = slack_team_factory()
        slack_user = slack_user_factory()
        slack_team_installation = slack_team_installation_factory.build(slack_team=slack_team, installer=slack_user)

        mutation = f'''
          mutation {{
            createSlackTeamInstallation(input: {{slackTeamId: "{slack_team.id}",
                                                 accessToken: "{slack_team_installation.access_token}",
                                                 scope: "{slack_team_installation.scope}",
                                                 installerId: "{slack_team_installation.installer.id}",
                                                 botUserId: "{slack_team_installation.bot_user_id}",
                                                 botAccessToken: "{slack_team_installation.bot_access_token}"}}) {{
              slackTeamInstallation {{
                accessToken
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackTeamInstallation'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_team(self, auth_client, slack_team_factory, slack_user_factory, slack_team_installation_factory):
        slack_team = slack_team_factory.build()
        slack_user = slack_user_factory()
        slack_team_installation = slack_team_installation_factory.build(slack_team=slack_team, installer=slack_user)

        mutation = f'''
          mutation {{
            createSlackTeamInstallation(input: {{slackTeamId: "{slack_team.id}",
                                                 accessToken: "{slack_team_installation.access_token}",
                                                 scope: "{slack_team_installation.scope}",
                                                 installerId: "{slack_team_installation.installer.id}",
                                                 botUserId: "{slack_team_installation.bot_user_id}",
                                                 botAccessToken: "{slack_team_installation.bot_access_token}"}}) {{
              slackTeamInstallation {{
                accessToken
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackTeamInstallation'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Slack Team Id'

    @pytest.mark.django_db
    def test_valid(self, auth_client, slack_team_factory, slack_user_factory, slack_team_installation_factory):
        slack_team = slack_team_factory()
        slack_user = slack_user_factory()
        slack_team_installation = slack_team_installation_factory.build(slack_team=slack_team, installer=slack_user)

        mutation = f'''
          mutation {{
            createSlackTeamInstallation(input: {{slackTeamId: "{slack_team.id}",
                                                 accessToken: "{slack_team_installation.access_token}",
                                                 scope: "{slack_team_installation.scope}",
                                                 installerId: "{slack_team_installation.installer.id}",
                                                 botUserId: "{slack_team_installation.bot_user_id}",
                                                 botAccessToken: "{slack_team_installation.bot_access_token}"}}) {{
              slackTeamInstallation {{
                accessToken
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackTeamInstallation']['slackTeamInstallation']['accessToken'] ==\
            slack_team_installation.access_token


class TestCreateMessageFromSlack:
    @pytest.mark.django_db
    def test_unauthenticated(self, client, session_factory, slack_channel_factory, user_factory, slack_user_factory,
                             slack_event_factory, message_factory):
        session = session_factory()
        slack_channel = slack_channel_factory(session=session)
        user = user_factory()
        slack_user = slack_user_factory(user=user)

        slack_event = slack_event_factory.build()
        message = message_factory.build()

        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{message.text}", time: "{message.time}",
                                            slackChannelId: "{slack_channel.id}", slackUserId: "{slack_user.id}",
                                            slackEventTs: "{slack_event.ts}"}}) {{
              message {{
                text
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_user(self, auth_client, session_factory, slack_channel_factory, user_factory,
                                slack_user_factory, slack_event_factory, message_factory):
        session = session_factory()
        slack_channel = slack_channel_factory.build(session=session)
        user = user_factory()
        slack_user = slack_user_factory.build(user=user)

        slack_event = slack_event_factory.build()
        message = message_factory.build()

        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{message.text}", time: "{message.time}",
                                            slackChannelId: "{slack_channel.id}", slackUserId: "{slack_user.id}",
                                            slackEventTs: "{slack_event.ts}"}}) {{
              message {{
                text
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Slack User Id'

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, session_factory, slack_channel_factory, user_factory,
                                   slack_user_factory, slack_event_factory, message_factory):
        session = session_factory()
        slack_channel = slack_channel_factory.build(session=session)
        user = user_factory()
        slack_user = slack_user_factory(user=user)

        slack_event = slack_event_factory.build()
        message = message_factory.build()

        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{message.text}", time: "{message.time}",
                                            slackChannelId: "{slack_channel.id}", slackUserId: "{slack_user.id}",
                                            slackEventTs: "{slack_event.ts}"}}) {{
              message {{
                text
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Slack Channel Id'

    @pytest.mark.django_db
    def test_valid(self, auth_client, session_factory, slack_channel_factory, user_factory,
                   slack_user_factory, slack_event_factory, message_factory):
        session = session_factory()
        slack_channel = slack_channel_factory(session=session)
        user = user_factory()
        slack_user = slack_user_factory(user=user)

        slack_event = slack_event_factory.build()
        message = message_factory.build()

        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{message.text}", time: "{message.time}",
                                            slackChannelId: "{slack_channel.id}", slackUserId: "{slack_user.id}",
                                            slackEventTs: "{slack_event.ts}"}}) {{
              message {{
                author {{
                  id
                }}
                session {{
                  id
                  participants {{
                    id
                  }}
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createMessageFromSlack']['message']['author']['id'] == \
            str(slack_user.user.id)
        assert response.json()['data']['createMessageFromSlack']['message']['session']['id'] == str(session.id)
        assert {'id': str(user.id)} in response.json()['data']['createMessageFromSlack']['message']['session'][
            'participants']


class TestCreateReplyFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, session_factory, slack_channel_factory, slack_event_factory,
                             slack_user_factory, message_factory, reply_factory):
        session = session_factory()
        slack_channel = slack_channel_factory(session=session)
        message_slack_event = slack_event_factory()
        reply_slack_event = slack_event_factory()
        message_slack_user = slack_user_factory()
        reply_slack_user = slack_user_factory()
        message = message_factory(session=session, slack_event=message_slack_event, author=message_slack_user.user)
        reply = reply_factory.build(message=message, slack_event=reply_slack_event, author=reply_slack_user.user)

        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{reply.text}", time: "{reply.time}",
                                          messageSlackEventTs: "{message_slack_event.ts}",
                                          slackChannelId: "{slack_channel.id}",
                                          slackUserId: "{reply_slack_user.id}",
                                          slackEventTs: "{reply_slack_event.ts}"}}) {{
              reply {{
                message {{
                  author {{
                    id
                  }}
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, session_factory, slack_channel_factory, slack_event_factory,
                                   slack_user_factory, message_factory, reply_factory):
        session = session_factory()
        slack_channel = slack_channel_factory.build(session=session)
        message_slack_event = slack_event_factory()
        reply_slack_event = slack_event_factory()
        message_slack_user = slack_user_factory()
        reply_slack_user = slack_user_factory()
        message = message_factory(session=session, slack_event=message_slack_event, author=message_slack_user.user)
        reply = reply_factory.build(message=message, slack_event=reply_slack_event, author=reply_slack_user.user)

        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{reply.text}", time: "{reply.time}",
                                          messageSlackEventTs: "{message_slack_event.ts}",
                                          slackChannelId: "{slack_channel.id}",
                                          slackUserId: "{reply_slack_user.id}",
                                          slackEventTs: "{reply_slack_event.ts}"}}) {{
              reply {{
                message {{
                  author {{
                    id
                  }}
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Slack Channel Id'

    @pytest.mark.django_db
    def test_invalid_slack_user(self, auth_client, session_factory, slack_channel_factory, slack_event_factory,
                                slack_user_factory, message_factory, reply_factory):
        session = session_factory()
        slack_channel = slack_channel_factory(session=session)
        message_slack_event = slack_event_factory()
        reply_slack_event = slack_event_factory()
        message_slack_user = slack_user_factory()
        reply_slack_user = slack_user_factory.build()
        message = message_factory(session=session, slack_event=message_slack_event, author=message_slack_user.user)
        reply = reply_factory.build(message=message, slack_event=reply_slack_event, author=reply_slack_user.user)

        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{reply.text}", time: "{reply.time}",
                                          messageSlackEventTs: "{message_slack_event.ts}",
                                          slackChannelId: "{slack_channel.id}",
                                          slackUserId: "{reply_slack_user.id}",
                                          slackEventTs: "{reply_slack_event.ts}"}}) {{
              reply {{
                message {{
                  author {{
                    id
                  }}
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Slack User Id'

    @pytest.mark.django_db
    def test_create_invalid_message_slack_event(self, auth_client, session_factory, slack_channel_factory,
                                                slack_event_factory, slack_user_factory, message_factory,
                                                reply_factory):
        session = session_factory()
        slack_channel = slack_channel_factory(session=session)
        message_slack_event = slack_event_factory()
        wrong_message_slack_event = slack_event_factory()
        reply_slack_event = slack_event_factory()
        message_slack_user = slack_user_factory()
        reply_slack_user = slack_user_factory()
        message = message_factory(session=session, slack_event=message_slack_event, author=message_slack_user.user)
        reply = reply_factory.build(message=message, slack_event=reply_slack_event, author=reply_slack_user.user)

        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{reply.text}", time: "{reply.time}",
                                          messageSlackEventTs: "{wrong_message_slack_event.ts}",
                                          slackChannelId: "{slack_channel.id}",
                                          slackUserId: "{reply_slack_user.id}",
                                          slackEventTs: "{reply_slack_event.ts}"}}) {{
              reply {{
                message {{
                  author {{
                    id
                  }}
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Message Slack Event Ts'

    @pytest.mark.django_db
    def test_valid(self, auth_client, session_factory, slack_channel_factory,
                   slack_event_factory, slack_user_factory, message_factory,
                   reply_factory):
        session = session_factory()
        slack_channel = slack_channel_factory(session=session)
        message_slack_event = slack_event_factory()
        reply_slack_event = slack_event_factory()
        message_slack_user = slack_user_factory()
        reply_slack_user = slack_user_factory()
        message = message_factory(session=session, slack_event=message_slack_event, author=message_slack_user.user)
        reply = reply_factory.build(message=message, slack_event=reply_slack_event, author=reply_slack_user.user)

        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{reply.text}", time: "{reply.time}",
                                          messageSlackEventTs: "{message_slack_event.ts}",
                                          slackChannelId: "{slack_channel.id}",
                                          slackUserId: "{reply_slack_user.id}",
                                          slackEventTs: "{reply_slack_event.ts}"}}) {{
              reply {{
                message {{
                  author {{
                    id
                  }}
                  session {{
                    participants {{
                      id
                    }}
                  }}
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReplyFromSlack']['reply']['message']['author']['id'] == \
            str(message.author.id)
        assert {'id': str(reply_slack_user.user.id)} in response.json()['data']['createReplyFromSlack']['reply'][
            'message']['session']['participants']


class TestGetOrCreateGroupFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, group_factory, slack_team_factory):
        group = group_factory.build()
        slack_team = slack_team_factory.build()

        mutation = f'''
          mutation {{
            getOrCreateGroupFromSlack(input: {{slackTeamId: "{slack_team.id}",
                                               slackTeamName: "{slack_team.name}",
                                               groupName: "{group.name}"}}) {{
              slackTeam {{
                group {{
                  name
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['getOrCreateGroupFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_id(self, auth_client, group_factory, slack_team_factory):
        group = group_factory()
        slack_team = slack_team_factory(group=group)

        mutation = f'''
          mutation {{
            getOrCreateGroupFromSlack(input: {{slackTeamId: "{slack_team.id}",
                                               slackTeamName: "{slack_team.name}",
                                               groupName: "{group.name}"}}) {{
              slackTeam {{
                group {{
                  name
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['getOrCreateGroupFromSlack'] is None
        assert response.json()['errors'][0]['message'] == f'Slack Team with id {slack_team.id} already exists'

    @pytest.mark.django_db
    def test_valid(self, auth_client, group_factory, slack_team_factory):
        group = group_factory()
        slack_team = slack_team_factory.build(group=group)

        mutation = f'''
          mutation {{
            getOrCreateGroupFromSlack(input: {{slackTeamId: "{slack_team.id}",
                                               slackTeamName: "{slack_team.name}",
                                               groupName: "{group.name}"}}) {{
               slackTeam {{
                 group {{
                   id
                 }}
               }}
             }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['getOrCreateGroupFromSlack']['slackTeam']['group']['id'] == str(group.id)


class TestGetOrCreateUserFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_team_factory, slack_user_factory):
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build(slack_team=slack_team)

        mutation = f'''
          mutation {{
            getOrCreateUserFromSlack(input: {{id: "{slack_user.id}",
                                              firstName: "{slack_user.first_name}",
                                              lastName: "{slack_user.last_name}",
                                              realName: "{slack_user.real_name}",
                                              displayName: "{slack_user.display_name}",
                                              email: "{slack_user.email}",
                                              avatar72: "{slack_user.avatar_72}",
                                              isBot: {str(slack_user.is_bot).lower()},
                                              isAdmin: {str(slack_user.is_admin).lower()},
                                              slackTeamId: "{slack_team.id}"}}) {{
              slackUser {{
                user {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['getOrCreateUserFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_existing_slack_user(self, auth_client, slack_team_factory, slack_user_factory):
        slack_team = slack_team_factory()
        slack_user = slack_user_factory(slack_team=slack_team)

        mutation = f'''
          mutation {{
            getOrCreateUserFromSlack(input: {{id: "{slack_user.id}",
                                              firstName: "{slack_user.first_name}",
                                              lastName: "{slack_user.last_name}",
                                              realName: "{slack_user.real_name}",
                                              displayName: "{slack_user.display_name}",
                                              email: "{slack_user.email}",
                                              avatar72: "{slack_user.avatar_72}",
                                              isBot: {str(slack_user.is_bot).lower()},
                                              isAdmin: {str(slack_user.is_admin).lower()},
                                              slackTeamId: "{slack_team.id}"}}) {{
              slackUser {{
                user {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['getOrCreateUserFromSlack'] is None
        assert response.json()['errors'][0]['message'] == f'Slack User with id {slack_user.id} already exists'

    @pytest.mark.django_db
    def test_valid_and_gets_user(self, auth_client, slack_team_factory, user_factory, slack_user_factory):
        slack_team = slack_team_factory()
        user = user_factory()
        slack_user = slack_user_factory.build(slack_team=slack_team, email=user.email)

        mutation = f'''
          mutation {{
            getOrCreateUserFromSlack(input: {{id: "{slack_user.id}",
                                              firstName: "{slack_user.first_name}",
                                              lastName: "{slack_user.last_name}",
                                              realName: "{slack_user.real_name}",
                                              displayName: "{slack_user.display_name}",
                                              email: "{slack_user.email}",
                                              avatar72: "{slack_user.avatar_72}",
                                              isBot: {str(slack_user.is_bot).lower()},
                                              isAdmin: {str(slack_user.is_admin).lower()},
                                              slackTeamId: "{slack_team.id}"}}) {{
              slackUser {{
                user {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['getOrCreateUserFromSlack']['slackUser']['user']['id'] == str(user.id)

    @pytest.mark.django_db
    def test_valid_and_creates_user(self, auth_client, slack_team_factory, user_factory, slack_user_factory):
        slack_team = slack_team_factory()
        user = user_factory.build()
        slack_user = slack_user_factory.build(slack_team=slack_team, email=user.email)

        mutation = f'''
          mutation {{
            getOrCreateUserFromSlack(input: {{id: "{slack_user.id}",
                                              firstName: "{slack_user.first_name}",
                                              lastName: "{slack_user.last_name}",
                                              realName: "{slack_user.real_name}",
                                              displayName: "{slack_user.display_name}",
                                              email: "{slack_user.email}",
                                              avatar72: "{slack_user.avatar_72}",
                                              isBot: {str(slack_user.is_bot).lower()},
                                              isAdmin: {str(slack_user.is_admin).lower()},
                                              slackTeamId: "{slack_team.id}"}}) {{
              slackUser {{
                user {{
                  email
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['getOrCreateUserFromSlack']['slackUser']['user']['email'] == slack_user.email


class TestSolveQuestionFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, user_factory, question_factory, session_factory,
                             slack_channel_factory, slack_user_factory):
        original_poster = user_factory()
        question = question_factory(original_poster=original_poster)
        session = session_factory(question=question)
        slack_channel = slack_channel_factory(session=session)
        time_end = session_factory.build().time_end
        slack_solver = slack_user_factory()

        mutation = f'''
          mutation {{
            solveQuestionFromSlack(input: {{slackChannelId: "{slack_channel.id}",
                                            slackUserId: "{slack_solver.id}",
                                            timeEnd: "{time_end}"}}) {{
              question {{
                session {{
                  timeEnd
                }}
                solver {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['solveQuestionFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, user_factory, question_factory, session_factory,
                                   slack_channel_factory, slack_user_factory):
        original_poster = user_factory()
        question = question_factory(original_poster=original_poster)
        session = session_factory(question=question)
        slack_channel = slack_channel_factory.build(session=session)
        time_end = session_factory.build().time_end
        slack_solver = slack_user_factory()

        mutation = f'''
          mutation {{
            solveQuestionFromSlack(input: {{slackChannelId: "{slack_channel.id}",
                                            slackUserId: "{slack_solver.id}",
                                            timeEnd: "{time_end}"}}) {{
              question {{
                session {{
                  timeEnd
                }}
                solver {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['solveQuestionFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Slack Channel Id'

    @pytest.mark.django_db
    def test_invalid_slack_user(self, auth_client, user_factory, question_factory,
                                session_factory, slack_channel_factory, slack_user_factory):
        original_poster = user_factory()
        question = question_factory(original_poster=original_poster)
        session = session_factory(question=question)
        slack_channel = slack_channel_factory(session=session)
        time_end = session_factory.build().time_end
        slack_solver = slack_user_factory.build()

        mutation = f'''
          mutation {{
            solveQuestionFromSlack(input: {{slackChannelId: "{slack_channel.id}",
                                            slackUserId: "{slack_solver.id}",
                                            timeEnd: "{time_end}"}}) {{
              question {{
                session {{
                  timeEnd
                }}
                solver {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['solveQuestionFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Slack User Id'

    @pytest.mark.django_db
    def test_valid(self, auth_client, user_factory, question_factory, session_factory,
                   slack_channel_factory, slack_user_factory):
        original_poster = user_factory()
        question = question_factory(original_poster=original_poster)
        session = session_factory(question=question)
        slack_channel = slack_channel_factory(session=session)
        time_end = session_factory.build().time_end
        slack_solver = slack_user_factory()

        mutation = f'''
          mutation {{
            solveQuestionFromSlack(input: {{slackChannelId: "{slack_channel.id}",
                                            slackUserId: "{slack_solver.id}",
                                            timeEnd: "{time_end}"}}) {{
              question {{
                session {{
                  timeEnd
                }}
                solver {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['solveQuestionFromSlack']['question'][
                   'solver']['id'] == str(slack_solver.user.id)


class TestAddToSlack:

    @pytest.mark.django_db
    @pytest.mark.parametrize('slack_oauth_request', ['invalid_token'], indirect=True)
    def test_invalid_token(self, client, slack_oauth_request):
        code = '123456789012.123456789012.1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ABCDEFGHIJKLMNOPQR'
        mutation = f'''
          mutation {{
            addToSlack(input: {{code: "{code}"}}) {{
              slackTeam {{
                name
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})
        assert response.status_code == 200
        assert response.json()['errors'][0]['message'] == 'Error accessing OAuth: invalid_code'

    @pytest.mark.django_db
    @pytest.mark.parametrize('slack_oauth_request', ['valid_token'], indirect=True)
    def test_valid(self, client, slack_oauth_request, slack_client_factory):
        code = '123456789012.123456789012.1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ABCDEFGHIJKLMNOPQR'
        mutation = f'''
          mutation {{
            addToSlack(input: {{code: "{code}"}}) {{
              slackTeam {{
                name
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})
        assert response.status_code == 200
        assert response.json()['data']['addToSlack']['slackTeam']['name'] == 'Clippy Sandbox'
