import graphene
from graphene_django.types import DjangoObjectType

from app.groups.models import Group, GroupSetting


class GroupType(DjangoObjectType):
    class Meta:
        model = Group


class GroupSettingType(DjangoObjectType):
    class Meta:
        model = GroupSetting


class GroupInputType(graphene.InputObjectType):
    name = graphene.String(required=True)


class GroupSettingInputType(graphene.InputObjectType):
    group_id = graphene.Int(required=True)
    name = graphene.String(required=True)
    value = graphene.String(required=True)
    data_type = graphene.String(required=True)
