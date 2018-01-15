import graphene

from app.users.models import User
from app.users.types import UserType


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(UserType)

    def resolve_user(self, info, id=None):
        if id is not None:
            return User.objects.get(pk=id)

        return None

    def resolve_users(self, info):
        return User.objects.all()
