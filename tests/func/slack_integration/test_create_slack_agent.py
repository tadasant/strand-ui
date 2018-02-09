import pytest
import requests


class TestCreateSlackAgent:

    @pytest.mark.django_db
    @pytest.mark.parametrize('slack_oauth_request', ['invalid_token'], indirect=True)
    def test_invalid_token(self, client, slack_oauth_request):
        code = '123456789012.123456789012.1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ABCDEFGHIJKLMNOPQR'
        mutation = f'''
          mutation {{
            createSlackAgent(input: {{code: "{code}"}}) {{
              slackAgent {{
                slackTeam {{
                  name
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})
        assert response.status_code == 200
        assert response.json()['errors'][0]['message'] == 'Error accessing OAuth: invalid_code'

    @pytest.mark.django_db
    @pytest.mark.parametrize('slack_oauth_request', ['valid_token'], indirect=True)
    def test_valid(self, client, slack_oauth_request, slack_client_factory, slack_app_request_factory):
        code = '123456789012.123456789012.1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ABCDEFGHIJKLMNOPQR'
        mutation = f'''
          mutation {{
            createSlackAgent(input: {{code: "{code}"}}) {{
              slackAgent {{
                slackTeam {{
                  name
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})
        assert response.status_code == 200
        assert response.json()['data']['createSlackAgent']['slackAgent']['slackTeam']['name'] == 'Clippy Sandbox'
        assert requests.post.call_count == 1
