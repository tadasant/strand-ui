import pytest


class TestCreateQuestion:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, question_factory, user_factory, group_factory):
        group = group_factory()
        user = user_factory()
        question = question_factory.build()

        mutation = f'''
          mutation {{
            createQuestion(input: {{title: "{question.title}", description: "{question.description}",
                                    isAnonymous: {str(question.is_anonymous).lower()},
                                    originalPosterId: {user.id},
                                    groupId: {str(group.id)}}}) {{
              question {{
                title
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createQuestion'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, auth_client, question_factory, user_factory, group_factory):
        group = group_factory()
        user = user_factory()
        question = question_factory.build()

        mutation = f'''
          mutation {{
            createQuestion(input: {{title: "{question.title}", description: "{question.description}",
                                    isAnonymous: {str(question.is_anonymous).lower()},
                                    originalPosterId: {user.id},
                                    groupId: {str(group.id)}}}) {{
              question {{
                title
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createQuestion']['question']['title'] == question.title

    @pytest.mark.django_db
    def test_valid_and_create_tags(self, auth_client, question_factory, user_factory, group_factory,
                                   tag_factory):
        group = group_factory()
        user = user_factory()
        question = question_factory.build()
        tag_one = tag_factory.build()
        tag_two = tag_factory.build()

        mutation = f'''
          mutation {{
            createQuestion(input: {{title: "{question.title}", description: "{question.description}",
                                    isAnonymous: {str(question.is_anonymous).lower()},
                                    originalPosterId: {user.id},
                                    groupId: {str(group.id)},
                                    tags: [
                                      {{name: "{tag_one.name}"}},
                                      {{name: "{tag_two.name}"}}
                                    ]}}) {{
              question {{
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
        assert response.json()['data']['createQuestion']['question']
        assert len(response.json()['data']['createQuestion']['question']['tags']) == 2
