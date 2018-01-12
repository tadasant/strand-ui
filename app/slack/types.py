import graphene
from graphene_django.types import DjangoObjectType

from app.slack.models import SlackUser, SlackChannel, SlackTeam, SlackSettings


class SlackUserType(DjangoObjectType):
    class Meta:
        model = SlackUser


class SlackUserInputType(graphene.InputObjectType):
    id = graphene.String(required=True)
    first_name = graphene.String()
    last_name = graphene.String()
    real_name = graphene.String(required=True)
    display_name = graphene.String(required=True)
    email = graphene.String()
    avatar_72 = graphene.String()
    is_bot = graphene.Boolean(required=True)
    is_admin = graphene.Boolean(required=True)

    slack_team_id = graphene.String(required=True)
    user_id = graphene.Int(required=True)



class SlackChannelType(DjangoObjectType):
    class Meta:
        model = SlackChannel


class SlackTeamType(DjangoObjectType):
    class Meta:
        model = SlackTeam


class SlackSettingsType(DjangoObjectType):
    class Meta:
        model = SlackSettings