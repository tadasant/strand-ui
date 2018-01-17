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
                                    isSolved: {str(question.is_solved).lower()},
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


class TestCreateTag:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, tag_factory):
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
    def test_valid(self, auth_client, tag_factory):
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
