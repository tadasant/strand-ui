import pytest


class TestCreateUserAndTopicFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, topic_factory, slack_user_factory, slack_team_factory, tag_factory):
        slack_user = slack_user_factory.build()
        slack_team = slack_team_factory()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        topic = topic_factory.build()

        mutation = f'''
          mutation {{
            createUserAndTopicFromSlack(input: {{title: "{topic.title}",
                                                    description: "{topic.description}",
                                                    isAnonymous: {str(topic.is_anonymous).lower()},
                                                    originalPosterSlackUser: {{
                                                      id: "{slack_user.id}",
                                                      name: "{slack_user.name}",
                                                      firstName: "{slack_user.first_name}",
                                                      lastName: "{slack_user.last_name}",
                                                      realName: "{slack_user.real_name}",
                                                      displayName: "{slack_user.display_name}",
                                                      email: "{slack_user.email}",
                                                      avatar72: "{slack_user.avatar_72}",
                                                      isBot: {str(slack_user.is_bot).lower()},
                                                      isAdmin: {str(slack_user.is_admin).lower()},
                                                      slackTeamId: "{slack_team.id}"
                                                    }},
                                                    tags: [
                                                      {{name: "{tag_one.name}"}},
                                                      {{name: "{tag_two.name}"}}
                                                    ]}}) {{
              topic {{
                title
                tags {{
                  name
                }}
              }}
              slackUser {{
                id
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndTopicFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_user(self, auth_client, topic_factory, slack_user_factory, slack_team_factory,
                                tag_factory):
        slack_user = slack_user_factory()
        slack_team = slack_team_factory()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        topic = topic_factory.build()

        mutation = f'''
          mutation {{
            createUserAndTopicFromSlack(input: {{title: "{topic.title}",
                                                    description: "{topic.description}",
                                                    isAnonymous: {str(topic.is_anonymous).lower()},
                                                    originalPosterSlackUser: {{
                                                      id: "{slack_user.id}",
                                                      name: "{slack_user.name}",
                                                      firstName: "{slack_user.first_name}",
                                                      lastName: "{slack_user.last_name}",
                                                      realName: "{slack_user.real_name}",
                                                      displayName: "{slack_user.display_name}",
                                                      email: "{slack_user.email}",
                                                      avatar72: "{slack_user.avatar_72}",
                                                      isBot: {str(slack_user.is_bot).lower()},
                                                      isAdmin: {str(slack_user.is_admin).lower()},
                                                      slackTeamId: "{slack_team.id}"
                                                    }},
                                                    tags: [
                                                      {{name: "{tag_one.name}"}},
                                                      {{name: "{tag_two.name}"}}
                                                    ]}}) {{
              topic {{
                title
                tags {{
                  name
                }}
              }}
              slackUser {{
                id
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndTopicFromSlack'] is None
        assert response.json()['errors'][0]['message'] == "{'id': ['slack user with this id already exists.']}"

    @pytest.mark.django_db
    def test_invalid_slack_team(self, auth_client, topic_factory, slack_user_factory, slack_team_factory,
                                tag_factory):
        slack_user = slack_user_factory.build()
        slack_team = slack_team_factory.build()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        topic = topic_factory.build()

        mutation = f'''
          mutation {{
            createUserAndTopicFromSlack(input: {{title: "{topic.title}",
                                                    description: "{topic.description}",
                                                    isAnonymous: {str(topic.is_anonymous).lower()},
                                                    originalPosterSlackUser: {{
                                                      id: "{slack_user.id}",
                                                      name: "{slack_user.name}",
                                                      firstName: "{slack_user.first_name}",
                                                      lastName: "{slack_user.last_name}",
                                                      realName: "{slack_user.real_name}",
                                                      displayName: "{slack_user.display_name}",
                                                      email: "{slack_user.email}",
                                                      avatar72: "{slack_user.avatar_72}",
                                                      isBot: {str(slack_user.is_bot).lower()},
                                                      isAdmin: {str(slack_user.is_admin).lower()},
                                                      slackTeamId: "{slack_team.id}"
                                                    }},
                                                    tags: [
                                                      {{name: "{tag_one.name}"}},
                                                      {{name: "{tag_two.name}"}}
                                                    ]}}) {{
              topic {{
                title
                tags {{
                  name
                }}
              }}
              slackUser {{
                id
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndTopicFromSlack'] is None
        assert response.json()['errors'][0]['message'] == f"{{'slack_team_id': ['Invalid pk \"{slack_team.id}\" - " \
                                                          "object does not exist.']}"

    @pytest.mark.django_db
    def test_valid(self, auth_client, topic_factory, slack_user_factory, slack_team_factory, tag_factory):
        slack_user = slack_user_factory.build()
        slack_team = slack_team_factory()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        topic = topic_factory.build()

        mutation = f'''
          mutation {{
            createUserAndTopicFromSlack(input: {{title: "{topic.title}",
                                                    description: "{topic.description}",
                                                    isAnonymous: {str(topic.is_anonymous).lower()},
                                                    originalPosterSlackUser: {{
                                                      id: "{slack_user.id}",
                                                      name: "{slack_user.name}",
                                                      firstName: "{slack_user.first_name}",
                                                      lastName: "{slack_user.last_name}",
                                                      realName: "{slack_user.real_name}",
                                                      displayName: "{slack_user.display_name}",
                                                      email: "{slack_user.email}",
                                                      avatar72: "{slack_user.avatar_72}",
                                                      isBot: {str(slack_user.is_bot).lower()},
                                                      isAdmin: {str(slack_user.is_admin).lower()},
                                                      slackTeamId: "{slack_team.id}"
                                                    }},
                                                    tags: [
                                                      {{name: "{tag_one.name}"}},
                                                      {{name: "{tag_two.name}"}}
                                                    ]}}) {{
              topic {{
                title
                tags {{
                  name
                }}
              }}
              slackUser {{
                id
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserAndTopicFromSlack']['slackUser']['id'] == slack_user.id
        assert response.json()['data']['createUserAndTopicFromSlack']['topic']['title'] == topic.title
        assert len(response.json()['data']['createUserAndTopicFromSlack']['topic']['tags']) == 2
