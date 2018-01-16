import graphene
from graphene_django.types import DjangoObjectType

from app.groups.models import Group, GroupSettings


class GroupType(DjangoObjectType):
    class Meta:
        model = Group


class GroupSettingsType(DjangoObjectType):
    class Meta:
        model = GroupSettings


class GroupInputType(graphene.InputObjectType):
    name = graphene.String(required=True)


class GroupSettingsInputType(graphene.InputObjectType):
    group_id = graphene.Int(required=True)
    is_public = graphene.Boolean(required=True)
