import graphene

from app.groups.models import Group, GroupSetting
from app.groups.types import GroupType, GroupSettingType, GroupInputType, GroupSettingInputType


class CreateGroupMutation(graphene.Mutation):
    class Arguments:
        input = GroupInputType(required=True)

    group = graphene.Field(GroupType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        group = Group.objects.create(**input)
        return CreateGroupMutation(group=group)


class CreateGroupSettingMutation(graphene.Mutation):
    class Arguments:
        input = GroupSettingInputType(required=True)

    group_setting = graphene.Field(GroupSettingType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not Group.objects.filter(pk=input.group_id).exists():
            raise Exception('Invalid Group Id')

        group_setting = GroupSetting.objects.create(**input)
        return CreateGroupSettingMutation(group_setting=group_setting)


class Mutation(graphene.ObjectType):
    create_group = CreateGroupMutation.Field()
    create_group_setting = CreateGroupSettingMutation.Field()
