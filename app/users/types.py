import graphene
from graphene_django.types import DjangoObjectType

from app.users.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User


class UserInputType(graphene.InputObjectType):
    email = graphene.String()
    username = graphene.String(required=True)
    avatar_url = graphene.String()