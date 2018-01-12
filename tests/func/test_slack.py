import graphene
import pytest

from app.slack.schema import Query


class TestSlackUserQuery():
    """Test slack user API queries"""

    @pytest.mark.django_db
    def test_get_slack_user(self, slack_user_factory):
        slack_user = slack_user_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
              slackUser(id: "%s") {
                firstName
              }
            }
        ''' % slack_user.id
        result = schema.execute(query)
        assert not result.errors
        assert result.data['slackUser']['firstName'] == slack_user.first_name

    @pytest.mark.django_db
    def test_get_slack_users(self, slack_user_factory):
        slack_user = slack_user_factory()
        another_slack_user = slack_user_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
               slackUsers {
                 displayName
               }
            }
        '''
        result = schema.execute(query)
        assert not result.errors
        assert len(result.data['slackUsers']) == 2


class TestSlackTeamQuery():
    """Test slack team queries"""

    @pytest.mark.django_db
    def test_get_slack_team(self, slack_team_factory):
        slack_team = slack_team_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
              slackTeam(id: "%s") {
                name
              }
            }
        ''' % slack_team.id
        result = schema.execute(query)
        assert not result.errors
        assert result.data['slackTeam']['name'] == slack_team.name

    @pytest.mark.django_db
    def test_get_slack_teams(self, slack_team_factory):
        slack_team = slack_team_factory()
        another_slack_team = slack_team_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
               slackTeams {
                 group {
                   name
                 }
               }
            }
        '''
        result = schema.execute(query)
        assert not result.errors
        assert len(result.data['slackTeams']) == 2


class TestSlackChannelQuery():
    """Test Slack Channel API queries"""
    @pytest.mark.django_db
    def test_get_slack_channel(self, slack_channel_factory):
        slack_channel = slack_channel_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
              slackChannel(id: "%s") {
                name
              }
            }
        ''' % slack_channel.id
        result = schema.execute(query)
        assert not result.errors
        assert result.data['slackChannel']['name'] == slack_channel.name

    @pytest.mark.django_db
    def test_get_slack_channels(self, slack_channel_factory):
        slack_channel = slack_channel_factory()
        another_slack_channel = slack_channel_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
               slackChannels {
                 name
               }
            }
        '''
        result = schema.execute(query)
        assert not result.errors
        assert len(result.data['slackChannels']) == 2


class TestSlackSettingsQuery():
    """Test Slack Settings API queries"""
    @pytest.mark.django_db
    def test_get_slack_settings(self, slack_settings_factory):
        slack_settings = slack_settings_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
              slackSettings(id: %s) {
                botToken
              }
            }
        ''' % slack_settings.id
        result = schema.execute(query)
        assert not result.errors
        assert result.data['slackSettings']['botToken'] == slack_settings.bot_token

    @pytest.mark.django_db
    def test_get_slacks_settings(self, slack_settings_factory):
        slack_settings = slack_settings_factory()
        another_slack_settings = slack_settings_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
               slacksSettings {
                 botToken
               }
            }
        '''
        result = schema.execute(query)
        assert not result.errors
        assert len(result.data['slacksSettings']) == 2