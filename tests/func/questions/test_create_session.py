import pytest


class TestCreateSession:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, question_factory, session_factory):
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
    def test_valid(self, auth_client, question_factory, session_factory):
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
