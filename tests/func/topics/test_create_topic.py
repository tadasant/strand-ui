import pytest


class TestCreateTopic:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, topic_factory, user_factory, group_factory):
        group = group_factory()
        user = user_factory()
        topic = topic_factory.build()

        mutation = f'''
          mutation {{
            createTopic(input: {{title: "{topic.title}", description: "{topic.description}",
                                    isAnonymous: {str(topic.is_anonymous).lower()},
                                    originalPosterId: {user.id},
                                    groupId: {str(group.id)}}}) {{
              topic {{
                title
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createTopic'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, auth_client, topic_factory, user_factory, group_factory):
        group = group_factory()
        user = user_factory()
        topic = topic_factory.build()

        mutation = f'''
          mutation {{
            createTopic(input: {{title: "{topic.title}", description: "{topic.description}",
                                    isAnonymous: {str(topic.is_anonymous).lower()},
                                    originalPosterId: {user.id},
                                    groupId: {str(group.id)}}}) {{
              topic {{
                title
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createTopic']['topic']['title'] == topic.title

    @pytest.mark.django_db
    def test_valid_and_create_tags(self, auth_client, topic_factory, user_factory, group_factory,
                                   tag_factory):
        group = group_factory()
        user = user_factory()
        topic = topic_factory.build()
        tag_one = tag_factory.build()
        tag_two = tag_factory.build()

        mutation = f'''
          mutation {{
            createTopic(input: {{title: "{topic.title}", description: "{topic.description}",
                                    isAnonymous: {str(topic.is_anonymous).lower()},
                                    originalPosterId: {user.id},
                                    groupId: {str(group.id)},
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
        assert response.json()['data']['createTopic']['topic']
        assert len(response.json()['data']['createTopic']['topic']['tags']) == 2
