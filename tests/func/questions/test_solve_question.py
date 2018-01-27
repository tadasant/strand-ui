import pytest


class TestSolveQuestion:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, user_factory, question_factory, session_factory):
        original_poster = user_factory()
        question = question_factory(original_poster=original_poster)
        session_factory(question=question)
        solver = user_factory()

        mutation = f'''
          mutation {{
            solveQuestion(input: {{id: {question.id},
                                   solverId: {solver.id}}}) {{
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
        assert response.json()['data']['solveQuestion'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_question(self, auth_client, user_factory, question_factory, session_factory):
        original_poster = user_factory()
        question = question_factory(original_poster=original_poster)
        session_factory(question=question)
        solver = user_factory()

        mutation = f'''
          mutation {{
            solveQuestion(input: {{id: 1,
                                   solverId: {solver.id}}}) {{
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
        assert response.json()['data']['solveQuestion'] is None
        assert response.json()['errors'][0]['message'] == 'Question matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_user(self, auth_client, user_factory, question_factory, session_factory):
        original_poster = user_factory()
        question = question_factory(original_poster=original_poster)
        session_factory(question=question)

        mutation = f'''
          mutation {{
            solveQuestion(input: {{id: {question.id},
                                   solverId: 1}}) {{
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
        assert response.json()['data']['solveQuestion'] is None
        assert response.json()['errors'][0]['message'] == 'User matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, user_factory, question_factory, session_factory):
        original_poster = user_factory()
        question = question_factory(original_poster=original_poster)
        session_factory(question=question)
        solver = user_factory()

        mutation = f'''
          mutation {{
            solveQuestion(input: {{id: {question.id},
                                   solverId: {solver.id}}}) {{
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
        assert response.json()['data']['solveQuestion']['question']['solver']['id'] == str(solver.id)
