import pytest


class TestCreateQuestionFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, question_factory, slack_user_factory, tag_factory):
        slack_user = slack_user_factory()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        question = question_factory.build(is_solved=False)

        mutation = f'''
          mutation {{
            createQuestionFromSlack(input: {{title: "{question.title}",
                                             description: "{question.description}",
                                             isSolved: {str(question.is_solved).lower()},
                                             isAnonymous: {str(question.is_anonymous).lower()},
                                             originalPosterSlackUserId: "{slack_user.id}",
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
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createQuestionFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_original_poster_slack_user(self, auth_client, question_factory, slack_user_factory, tag_factory):
        slack_user = slack_user_factory.build()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        question = question_factory.build(is_solved=False)

        mutation = f'''
          mutation {{
            createQuestionFromSlack(input: {{title: "{question.title}",
                                             description: "{question.description}",
                                             isSolved: {str(question.is_solved).lower()},
                                             isAnonymous: {str(question.is_anonymous).lower()},
                                             originalPosterSlackUserId: "{slack_user.id}",
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
        assert response.json()['data']['createQuestionFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'SlackUser matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, question_factory, slack_user_factory, tag_factory):
        slack_user = slack_user_factory()
        tag_one = tag_factory()
        tag_two = tag_factory.build()
        question = question_factory.build(is_solved=False)

        mutation = f'''
          mutation {{
            createQuestionFromSlack(input: {{title: "{question.title}",
                                             description: "{question.description}",
                                             isSolved: {str(question.is_solved).lower()},
                                             isAnonymous: {str(question.is_anonymous).lower()},
                                             originalPosterSlackUserId: "{slack_user.id}",
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
        print(response.content)

        assert response.status_code == 200
        assert len(response.json()['data']['createQuestionFromSlack']['question']['tags']) == 2
        assert response.json()['data']['createQuestionFromSlack']['question']['title'] == question.title
