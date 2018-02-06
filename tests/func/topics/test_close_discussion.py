import pytest


class TestCloseDiscussion:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, discussion_factory):
        discussion = discussion_factory()

        mutation = f'''
          mutation {{
            closeDiscussion(input: {{id: {discussion.id}}}) {{
              discussion {{
                timeEnd
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['closeDiscussion'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_discussion(self, auth_client, discussion_factory):
        discussion = discussion_factory()

        mutation = f'''
          mutation {{
            closeDiscussion(input: {{id: {discussion.id + 1}}}) {{
              discussion {{
                timeEnd
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['closeDiscussion'] is None
        assert response.json()['errors'][0]['message'] == 'Discussion matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, discussion_factory):
        discussion = discussion_factory()

        mutation = f'''
          mutation {{
            closeDiscussion(input: {{id: {discussion.id}}}) {{
              discussion {{
                id
                timeEnd
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['closeDiscussion']['discussion']['id'] == str(discussion.id)
