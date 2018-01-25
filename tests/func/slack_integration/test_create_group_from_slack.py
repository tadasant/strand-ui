import pytest


class TestCreateGroupFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, group_factory, slack_team_factory):
        group = group_factory.build()
        slack_team = slack_team_factory.build()

        mutation = f'''
          mutation {{
            createGroupFromSlack(input: {{slackTeamId: "{slack_team.id}",
                                          slackTeamName: "{slack_team.name}",
                                          groupName: "{group.name}"}}) {{
              slackTeam {{
                group {{
                  name
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createGroupFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_id(self, auth_client, group_factory, slack_team_factory):
        group = group_factory()
        slack_team = slack_team_factory(group=group)

        mutation = f'''
          mutation {{
            createGroupFromSlack(input: {{slackTeamId: "{slack_team.id}",
                                          slackTeamName: "{slack_team.name}",
                                          groupName: "{group.name}"}}) {{
              slackTeam {{
                group {{
                  name
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createGroupFromSlack'] is None
        assert response.json()['errors'][0]['message'] == "{'id': ['slack team with this id already exists.']}"

    @pytest.mark.django_db
    def test_valid(self, auth_client, group_factory, slack_team_factory):
        group = group_factory()
        slack_team = slack_team_factory.build(group=group)

        mutation = f'''
          mutation {{
            createGroupFromSlack(input: {{slackTeamId: "{slack_team.id}",
                                          slackTeamName: "{slack_team.name}",
                                          groupName: "{group.name}"}}) {{
               slackTeam {{
                 group {{
                   id
                 }}
               }}
             }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createGroupFromSlack']['slackTeam']['group']['id'] == str(group.id)
