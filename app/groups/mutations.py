import graphene

from app.groups.models import Group, GroupSettings
from app.groups.types import GroupType, GroupSettingsType, GroupInputType, GroupSettingsInputType


class CreateGroupMutation(graphene.Mutation):
    class Arguments:
        input = GroupInputType(required=True)

    group = graphene.Field(GroupType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        group = Group.objects.create(**input)
        return CreateGroupMutation(group=group)


class CreateGroupSettingsMutation(graphene.Mutation):
    class Arguments:
        input = GroupSettingsInputType(required=True)

    group_settings = graphene.Field(GroupSettingsType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        if not Group.objects.filter(pk=input.group_id).exists():
            raise Exception('Invalid Group Id')

        group_settings = GroupSettings.objects.create(**input)
        return CreateGroupSettingsMutation(group_settings=group_settings)


class Mutation(graphene.ObjectType):
    create_group = CreateGroupMutation.Field()
    create_group_settings = CreateGroupSettingsMutation.Field()
