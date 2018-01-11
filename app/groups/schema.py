import graphene
from graphene_django.types import DjangoObjectType

from app.groups.models import Group, GroupSettings


class GroupType(DjangoObjectType):
    class Meta:
        model = Group


class GroupSettingsType(DjangoObjectType):
    class Meta:
        model = GroupSettings


class Query(object):
    group = graphene.Field(GroupType, id=graphene.Int(), name=graphene.String())
    group_settings = graphene.Field(GroupSettingsType, id=graphene.Int())

    all_groups = graphene.List(GroupType)
    all_group_settings = graphene.List(GroupSettingsType)

    def resolve_group(self, info, id=None, name=None):
        if id is not None:
            return Group.objects.get(pk=id)

        if name is not None:
            return Group.objects.get(name=name)

        return None

    def resolve_group_settings(self, info, id=None):
        if id is not None:
            return GroupSettings.objects.get(pk=id)

        return None

    def resolve_all_groups(self, info):
        return Group.objects.all()

    def resolve_all_group_settings(self, info):
        return GroupSettings.objects.all()