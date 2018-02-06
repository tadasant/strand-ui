import pytest


class TestCreateTopicFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, topic_factory, slack_user_factory, tag_factory):
        slack_user = slack_user_factory()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        topic = topic_factory.build()

        mutation = f'''
          mutation {{
            createTopicFromSlack(input: {{title: "{topic.title}",
                                             description: "{topic.description}",
                                             isAnonymous: {str(topic.is_anonymous).lower()},
                                             originalPosterSlackUserId: "{slack_user.id}",
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
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createTopicFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_original_poster_slack_user(self, auth_client, topic_factory, slack_user_factory, tag_factory):
        slack_user = slack_user_factory.build()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        topic = topic_factory.build()

        mutation = f'''
          mutation {{
            createTopicFromSlack(input: {{title: "{topic.title}",
                                             description: "{topic.description}",
                                             isAnonymous: {str(topic.is_anonymous).lower()},
                                             originalPosterSlackUserId: "{slack_user.id}",
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
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createTopicFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'SlackUser matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, topic_factory, slack_user_factory, tag_factory):
        slack_user = slack_user_factory()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        topic = topic_factory.build()

        mutation = f'''
          mutation {{
            createTopicFromSlack(input: {{title: "{topic.title}",
                                             description: "{topic.description}",
                                             isAnonymous: {str(topic.is_anonymous).lower()},
                                             originalPosterSlackUserId: "{slack_user.id}",
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
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        print(response.content)

        assert response.status_code == 200
        assert len(response.json()['data']['createTopicFromSlack']['topic']['tags']) == 2
        assert response.json()['data']['createTopicFromSlack']['topic']['title'] == topic.title
