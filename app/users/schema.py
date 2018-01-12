import graphene
from graphene_django.types import DjangoObjectType

from app.users.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(UserType)

    def resolve_user(self, info, id=None):
        if id is not None:
            return User.objects.get(pk=id)

        return None

    def resolve_users(self, info):
        return User.objects.all()
