import pytest


class TestQuestionMutations:

    @pytest.mark.django_db
    def test_create_question_unauthenticated(self, client, question_factory, user_factory, group_factory):
        group = group_factory()
        user = user_factory()
        question = question_factory.build()

        mutation = f'''
          mutation {{
            createQuestion(input: {{title: "{question.title}", description: "{question.description}",
                                    isSolved: {str(question.is_solved).lower()},
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
        print(response.content)
        assert response.status_code == 200
        assert response.json()['data']['createQuestion'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_question(self, auth_client, question_factory, user_factory, group_factory):
        group = group_factory()
        user = user_factory()
        question = question_factory.build()

        mutation = f'''
          mutation {{
            createQuestion(input: {{title: "{question.title}", description: "{question.description}",
                                    isSolved: {str(question.is_solved).lower()},
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


class TestSessionMutations:

    @pytest.mark.django_db
    def test_create_session_unauthenticated(self, client, question_factory, session_factory):
        question = question_factory()
        session = session_factory.build()

        mutation = f'''
          mutation {{
            createSession(input: {{timeStart: "{session.time_start}", timeEnd: "{session.time_end}",
                                   questionId: {question.id}}}) {{
              session {{
                question {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSession'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_session(self, auth_client, question_factory, session_factory):
        question = question_factory()
        session = session_factory.build()

        mutation = f'''
          mutation {{
            createSession(input: {{timeStart: "{session.time_start}", timeEnd: "{session.time_end}",
                                   questionId: {question.id}}}) {{
              session {{
                question {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSession']['session']['question']['id'] == str(question.id)


class TestTagMutations:

    @pytest.mark.django_db
    def test_create_tag_unauthenticated(self, client, tag_factory):
        tag = tag_factory.build()

        mutation = f'''
          mutation {{
            createTag(input: {{name: "{tag.name}"}}) {{
              tag {{
                name
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createTag'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_session(self, auth_client, tag_factory):
        tag = tag_factory.build()

        mutation = f'''
          mutation {{
            createTag(input: {{name: "{tag.name}"}}) {{
              tag {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createTag']['tag']['name'] == tag.name
