import pytest


class TestSlackTeamMutations():
    """Test slack team mutations"""

    @pytest.mark.django_db
    def test_create_slack_team_unauthenticated(self, client, group_factory):
        group = group_factory()

        mutation = f'''
          mutation {{
            createSlackTeam(input: {{id: "1", name: "dj", groupId: {group.id}}}) {{
              slackTeam {{
                name
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})
        print(response.content)
        assert response.status_code == 200
        assert response.json()['data']['createSlackTeam'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_slack_team_invalid_group(self, auth_client):
        mutation = '''
          mutation {
            createSlackTeam(input: {id: "1", name: "dj", groupId: 1}) {
              slackTeam {
                name
              }
            } 
          }
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        print(response.content)
        assert response.status_code == 200
        assert response.json()['data']['createSlackTeam'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Group Id'

    @pytest.mark.django_db
    def test_create_slack_team(self, auth_client, group_factory):
        group = group_factory()

        mutation = f'''
          mutation {{
            createSlackTeam(input: {{id: "1", name: "dj", groupId: {group.id} }}) {{
              slackTeam {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackTeam']['slackTeam']['name'] == 'dj'


class TestSlackUserMutations():
    """Test slack user mutations"""

    @pytest.mark.django_db
    def test_create_slack_user_unauthenticated(self, client, user_factory, slack_team_factory):
        user = user_factory()
        slack_team = slack_team_factory()

        mutation = f'''
          mutation {{
            createSlackUser(input: {{id: "1", realName: "John Doe", displayName: "johndoe", isBot: false,
                                     isAdmin: false, slackTeamId: "{slack_team.id}", userId: {user.id}}}) {{
              slackUser {{
                realName
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_slack_user_invalid_team(self, auth_client, user_factory):
        user = user_factory()

        mutation = f'''
          mutation {{
            createSlackUser(input: {{id: "1", realName: "John Doe", displayName: "johndoe", isBot: false,
                                     isAdmin: false, slackTeamId: "123AAA", userId: {user.id}}}) {{
              slackUser {{
                realName
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['errors'][0]['message'] == 'Invalid Slack Team Id'

    @pytest.mark.django_db
    def test_create_slack_user_invalid_user(self, auth_client, slack_team_factory):
        slack_team = slack_team_factory()

        mutation = f'''
          mutation {{
            createSlackUser(input: {{id: "1", realName: "John Doe", displayName: "johndoe", isBot: false,
                                     isAdmin: false, slackTeamId: "{slack_team.id}", userId: 0}}) {{
              slackUser {{
                realName
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['errors'][0]['message'] == 'Invalid User Id'

    @pytest.mark.django_db
    def test_create_slack_user(self, auth_client, user_factory, slack_team_factory):
        user = user_factory()
        slack_team = slack_team_factory()

        mutation = f'''
          mutation {{
            createSlackUser(input: {{id: "1", realName: "John Doe", displayName: "johndoe", isBot: false,
                                     isAdmin: false, slackTeamId: "{slack_team.id}", userId: {user.id}}}) {{
              slackUser {{
                realName
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackUser']['slackUser']['realName'] == 'John Doe'


class TestSlackChannelMutations():
    """Test slack channel mutations"""

    @pytest.mark.django_db
    def test_create_slack_channel_unauthenticated(self, client, slack_team_factory, session_factory):
        session = session_factory()
        slack_team = slack_team_factory()

        mutation = f'''
          mutation {{
            createSlackChannel(input: {{id: "1", name: "realtalk", slackTeamId: "{slack_team.id}",
                                        sessionId: {session.id}}}) {{
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_slack_channel_invalid_team(self, auth_client, session_factory):
        session = session_factory()

        mutation = f'''
          mutation {{
            createSlackChannel(input: {{id: "1", name: "realtalk", slackTeamId: "111AAA",
                                        sessionId: {session.id}}}) {{
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Slack Team Id'

    @pytest.mark.django_db
    def test_create_slack_channel_invalid_session(self, auth_client, slack_team_factory):
        slack_team = slack_team_factory()

        mutation = f'''
          mutation {{
            createSlackChannel(input: {{id: "1", name: "realtalk", slackTeamId: "{slack_team.id}",
                                        sessionId: 0}}) {{
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Session Id'

    @pytest.mark.django_db
    def test_create_slack_channel(self, auth_client, slack_team_factory, session_factory):
        slack_team = slack_team_factory()
        session = session_factory()

        mutation = f'''
          mutation {{
            createSlackChannel(input: {{id: "1", name: "realtalk", slackTeamId: "{slack_team.id}",
                                        sessionId: {session.id}}}) {{
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel']['slackChannel']['name'] == 'realtalk'


class TestSlackSettingsMutations():
    """Test slack team mutations"""

    @pytest.mark.django_db
    def test_create_slack_settings_unauthenticated(self, client, slack_team_factory):
        slack_team = slack_team_factory()

        mutation = f'''
          mutation {{
            createSlackSettings(input: {{botToken: "123AAA", slackTeamId: "{slack_team.id}"}}) {{
              slackSettings {{
                botToken
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackSettings'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_slack_settings_invalid_team(self, auth_client):
        mutation = f'''
          mutation {{
            createSlackSettings(input: {{botToken: "123AAA", slackTeamId: "123AAA"}}) {{
              slackSettings {{
                botToken
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackSettings'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Slack Team Id'

    @pytest.mark.django_db
    def test_create_slack_settings(self, auth_client, slack_team_factory):
        slack_team = slack_team_factory()

        mutation = f'''
          mutation {{
            createSlackSettings(input: {{botToken: "123AAA", slackTeamId: "{slack_team.id}"}}) {{
              slackSettings {{
                botToken
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackSettings']['slackSettings']['botToken'] == '123AAA'
