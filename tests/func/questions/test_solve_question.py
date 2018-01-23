import pytest


class TestSolveQuestion:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, user_factory, question_factory, session_factory):
        original_poster = user_factory()
        question = question_factory(original_poster=original_poster)
        session_factory(question=question)
        time_end = session_factory.build().time_end
        solver = user_factory()

        mutation = f'''
          mutation {{
            solveQuestion(input: {{questionId: {question.id},
                                   solverId: {solver.id},
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
        assert response.json()['data']['solveQuestion'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_question(self, auth_client, user_factory, question_factory, session_factory):
        original_poster = user_factory()
        question = question_factory(original_poster=original_poster)
        session_factory(question=question)
        time_end = str(session_factory.build().time_end)
        solver = user_factory()

        mutation = f'''
          mutation {{
            solveQuestion(input: {{questionId: 1,
                                   solverId: {solver.id},
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
        assert response.json()['data']['solveQuestion'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Question Id'

    @pytest.mark.django_db
    def test_invalid_user(self, auth_client, user_factory, question_factory, session_factory):
        original_poster = user_factory()
        question = question_factory(original_poster=original_poster)
        session_factory(question=question)
        time_end = str(session_factory.build().time_end)

        mutation = f'''
          mutation {{
            solveQuestion(input: {{questionId: {question.id},
                                   solverId: 1,
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
        assert response.json()['data']['solveQuestion'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid User Id'

    @pytest.mark.django_db
    def test_valid(self, auth_client, user_factory, question_factory, session_factory):
        original_poster = user_factory()
        question = question_factory(original_poster=original_poster)
        session_factory(question=question)
        solver = user_factory()
        time_end = session_factory.build().time_end

        mutation = f'''
          mutation {{
            solveQuestion(input: {{questionId: {question.id},
                                   solverId: {solver.id},
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
        assert response.json()['data']['solveQuestion']['question']['solver']['id'] == str(solver.id)
