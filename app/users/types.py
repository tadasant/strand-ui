import graphene
from graphene_django.types import DjangoObjectType

from app.users.models import User
from app.api.authorization import check_authorization


class UserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ('id', 'alias', 'slack_users',
                       'messages', 'replies', 'topics')

    @check_authorization
    def resolve_slack_users(self, info):
        return self.slack_users


class UserInputType(graphene.InputObjectType):
    email = graphene.String()
    username = graphene.String(required=True)
    avatar_url = graphene.String()
