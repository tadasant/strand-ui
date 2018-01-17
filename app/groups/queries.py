import graphene

from app.groups.models import Group, GroupSetting
from app.groups.types import GroupType, GroupSettingType


class Query(graphene.ObjectType):
    group = graphene.Field(GroupType, id=graphene.Int(), name=graphene.String())
    group_setting = graphene.Field(GroupSettingType, id=graphene.Int())

    groups = graphene.List(GroupType)
    group_settings = graphene.List(GroupSettingType)

    def resolve_group(self, info, id=None, name=None):
        if id is not None:
            return Group.objects.get(pk=id)

        if name is not None:
            return Group.objects.get(name=name)

        return None

    def resolve_group_setting(self, info, id=None):
        if id is not None:
            return GroupSetting.objects.get(pk=id)

        return None

    def resolve_groups(self, info):
        return Group.objects.all()

    def resolve_group_settings(self, info):
        return GroupSetting.objects.all()
