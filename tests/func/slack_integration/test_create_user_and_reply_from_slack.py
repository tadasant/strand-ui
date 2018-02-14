import pytest


class TestCreateUserAndReplyFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, message_factory, reply_factory, slack_event_factory,
                             discussion_factory, slack_channel_factory, slack_user_factory, slack_team_factory):
        discussion = discussion_factory()
        slack_channel = slack_channel_factory(discussion=discussion)
        message_slack_event = slack_event_factory()
        message = message_factory(origin_slack_event=message_slack_event, discussion=discussion)
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        reply_slack_event = slack_event_factory.build()
        reply = reply_factory.build(origin_slack_event=reply_slack_event, message=message)

        mutation = f'''
          mutation {{
            createUserAndReplyFromSlack(input: {{slackUser: {{
                                                   id: "{slack_user.id}",
                                                   name: "{slack_user.name}",
                                                   firstName: "{slack_user.first_name}",
                                                   lastName: "{slack_user.last_name}",
                                                   realName: "{slack_user.real_name}",
                                                   displayName: "{slack_user.display_name}",
                                                   email: "{slack_user.email}",
                                                   image72: "{slack_user.image_72}",
                                                   isBot: {str(slack_user.is_bot).lower()},
                                                   isAdmin: {str(slack_user.is_admin).lower()},
                                                   slackTeamId: "{slack_user.slack_team.id}"
                                                 }},
                                                 messageOriginSlackEventTs: "{reply.message.origin_slack_event.ts}",
                                                 originSlackEventTs: "{reply.origin_slack_event.ts}",
                                                 slackChannelId: "{slack_channel.id}",
                                                 text: "{reply.text}"}}) {{
              slackUser {{
                id
              }}
              user {{
                alias
              }}
              reply {{
                message {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_user(self, auth_client, message_factory, reply_factory, slack_event_factory,
                                discussion_factory, slack_channel_factory, slack_user_factory, slack_team_factory):
        discussion = discussion_factory()
        slack_channel = slack_channel_factory.build(discussion=discussion)
        message_slack_event = slack_event_factory()
        message = message_factory(origin_slack_event=message_slack_event, discussion=discussion)
        slack_team = slack_team_factory()
        slack_user = slack_user_factory(slack_team=slack_team)
        reply_slack_event = slack_event_factory.build()
        reply = reply_factory.build(origin_slack_event=reply_slack_event, message=message)

        mutation = f'''
          mutation {{
            createUserAndReplyFromSlack(input: {{slackUser: {{
                                                   id: "{slack_user.id}",
                                                   name: "{slack_user.name}",
                                                   firstName: "{slack_user.first_name}",
                                                   lastName: "{slack_user.last_name}",
                                                   realName: "{slack_user.real_name}",
                                                   displayName: "{slack_user.display_name}",
                                                   email: "{slack_user.email}",
                                                   image72: "{slack_user.image_72}",
                                                   isBot: {str(slack_user.is_bot).lower()},
                                                   isAdmin: {str(slack_user.is_admin).lower()},
                                                   slackTeamId: "{slack_user.slack_team.id}"
                                                 }},
                                                 messageOriginSlackEventTs: "{reply.message.origin_slack_event.ts}",
                                                 originSlackEventTs: "{reply.origin_slack_event.ts}",
                                                 slackChannelId: "{slack_channel.id}",
                                                 text: "{reply.text}"}}) {{
              slackUser {{
                id
              }}
              user {{
                alias
              }}
              reply {{
                message {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == "{'id': ['slack user with this id already exists.']}"

    @pytest.mark.django_db
    def test_invalid_slack_team(self, auth_client, message_factory, reply_factory, slack_event_factory,
                                discussion_factory, slack_channel_factory, slack_user_factory, slack_team_factory):
        discussion = discussion_factory()
        slack_channel = slack_channel_factory.build(discussion=discussion)
        message_slack_event = slack_event_factory()
        message = message_factory(origin_slack_event=message_slack_event, discussion=discussion)
        slack_team = slack_team_factory.build()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        reply_slack_event = slack_event_factory.build()
        reply = reply_factory.build(origin_slack_event=reply_slack_event, message=message)

        mutation = f'''
          mutation {{
            createUserAndReplyFromSlack(input: {{slackUser: {{
                                                   id: "{slack_user.id}",
                                                   name: "{slack_user.name}",
                                                   firstName: "{slack_user.first_name}",
                                                   lastName: "{slack_user.last_name}",
                                                   realName: "{slack_user.real_name}",
                                                   displayName: "{slack_user.display_name}",
                                                   email: "{slack_user.email}",
                                                   image72: "{slack_user.image_72}",
                                                   isBot: {str(slack_user.is_bot).lower()},
                                                   isAdmin: {str(slack_user.is_admin).lower()},
                                                   slackTeamId: "{slack_user.slack_team.id}"
                                                 }},
                                                 messageOriginSlackEventTs: "{reply.message.origin_slack_event.ts}",
                                                 originSlackEventTs: "{reply.origin_slack_event.ts}",
                                                 slackChannelId: "{slack_channel.id}",
                                                 text: "{reply.text}"}}) {{
              slackUser {{
                id
              }}
              user {{
                alias
              }}
              reply {{
                message {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == f"{{'slack_team_id': ['Invalid pk \"{slack_team.id}\" - " \
                                                          "object does not exist.']}"

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, message_factory, reply_factory, slack_event_factory,
                                   discussion_factory, slack_channel_factory, slack_user_factory, slack_team_factory):
        discussion = discussion_factory()
        slack_channel = slack_channel_factory.build(discussion=discussion)
        message_slack_event = slack_event_factory()
        message = message_factory(origin_slack_event=message_slack_event, discussion=discussion)
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        reply_slack_event = slack_event_factory.build()
        reply = reply_factory.build(origin_slack_event=reply_slack_event, message=message)

        mutation = f'''
          mutation {{
            createUserAndReplyFromSlack(input: {{slackUser: {{
                                                   id: "{slack_user.id}",
                                                   name: "{slack_user.name}",
                                                   firstName: "{slack_user.first_name}",
                                                   lastName: "{slack_user.last_name}",
                                                   realName: "{slack_user.real_name}",
                                                   displayName: "{slack_user.display_name}",
                                                   email: "{slack_user.email}",
                                                   image72: "{slack_user.image_72}",
                                                   isBot: {str(slack_user.is_bot).lower()},
                                                   isAdmin: {str(slack_user.is_admin).lower()},
                                                   slackTeamId: "{slack_user.slack_team.id}"
                                                 }},
                                                 messageOriginSlackEventTs: "{reply.message.origin_slack_event.ts}",
                                                 originSlackEventTs: "{reply.origin_slack_event.ts}",
                                                 slackChannelId: "{slack_channel.id}",
                                                 text: "{reply.text}"}}) {{
              slackUser {{
                id
              }}
              user {{
                alias
              }}
              reply {{
                message {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Message matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_message(self, auth_client, message_factory, reply_factory, slack_event_factory,
                             discussion_factory, slack_channel_factory, slack_user_factory, slack_team_factory):
        discussion = discussion_factory()
        slack_channel = slack_channel_factory(discussion=discussion)
        message_slack_event = slack_event_factory.build()
        message = message_factory.build(origin_slack_event=message_slack_event, discussion=discussion)
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        reply_slack_event = slack_event_factory.build()
        reply = reply_factory.build(origin_slack_event=reply_slack_event, message=message)

        mutation = f'''
          mutation {{
            createUserAndReplyFromSlack(input: {{slackUser: {{
                                                   id: "{slack_user.id}",
                                                   name: "{slack_user.name}",
                                                   firstName: "{slack_user.first_name}",
                                                   lastName: "{slack_user.last_name}",
                                                   realName: "{slack_user.real_name}",
                                                   displayName: "{slack_user.display_name}",
                                                   email: "{slack_user.email}",
                                                   image72: "{slack_user.image_72}",
                                                   isBot: {str(slack_user.is_bot).lower()},
                                                   isAdmin: {str(slack_user.is_admin).lower()},
                                                   slackTeamId: "{slack_user.slack_team.id}"
                                                 }},
                                                 messageOriginSlackEventTs: "{reply.message.origin_slack_event.ts}",
                                                 originSlackEventTs: "{reply.origin_slack_event.ts}",
                                                 slackChannelId: "{slack_channel.id}",
                                                 text: "{reply.text}"}}) {{
              slackUser {{
                id
              }}
              user {{
                alias
              }}
              reply {{
                message {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Message matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, message_factory, reply_factory, slack_event_factory,
                   discussion_factory, slack_channel_factory, slack_user_factory, slack_team_factory):
        discussion = discussion_factory()
        slack_channel = slack_channel_factory(discussion=discussion)
        message_slack_event = slack_event_factory()
        message = message_factory(origin_slack_event=message_slack_event, discussion=discussion)
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build(slack_team=slack_team)
        reply_slack_event = slack_event_factory.build()
        reply = reply_factory.build(origin_slack_event=reply_slack_event, message=message)

        mutation = f'''
          mutation {{
            createUserAndReplyFromSlack(input: {{slackUser: {{
                                                   id: "{slack_user.id}",
                                                   name: "{slack_user.name}",
                                                   firstName: "{slack_user.first_name}",
                                                   lastName: "{slack_user.last_name}",
                                                   realName: "{slack_user.real_name}",
                                                   displayName: "{slack_user.display_name}",
                                                   email: "{slack_user.email}",
                                                   image72: "{slack_user.image_72}",
                                                   isBot: {str(slack_user.is_bot).lower()},
                                                   isAdmin: {str(slack_user.is_admin).lower()},
                                                   slackTeamId: "{slack_user.slack_team.id}"
                                                 }},
                                                 messageOriginSlackEventTs: "{reply.message.origin_slack_event.ts}",
                                                 originSlackEventTs: "{reply.origin_slack_event.ts}",
                                                 slackChannelId: "{slack_channel.id}",
                                                 text: "{reply.text}"}}) {{
              slackUser {{
                id
              }}
              user {{
                alias
              }}
              reply {{
                message {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndReplyFromSlack']['slackUser']['id'] == slack_user.id
        assert response.json()['data']['createUserAndReplyFromSlack']['user']['alias']
        assert response.json()['data']['createUserAndReplyFromSlack']['reply']['message']['id'] == str(message.id)
