import graphene
from graphene_django.types import DjangoObjectType

from app.groups.models import Group


class GroupType(DjangoObjectType):
    class Meta:
        model = Group


class GroupInputType(graphene.InputObjectType):
    name = graphene.String(required=True)
