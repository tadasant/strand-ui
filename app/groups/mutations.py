import graphene

from app.groups.models import Group
from app.groups.types import GroupType, GroupInputType


class CreateGroupMutation(graphene.Mutation):
    class Arguments:
        input = GroupInputType(required=True)

    group = graphene.Field(GroupType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        group = Group.objects.create(**input)
        return CreateGroupMutation(group=group)


class Mutation(graphene.ObjectType):
    create_group = CreateGroupMutation.Field()
