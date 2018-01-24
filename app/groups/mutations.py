import graphene

from app.groups.serializers import GroupSerializer
from app.groups.types import GroupType, GroupInputType


class CreateGroupMutation(graphene.Mutation):
    class Arguments:
        input = GroupInputType(required=True)

    group = graphene.Field(GroupType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        group_serializer = GroupSerializer(data=input)
        group_serializer.is_valid(raise_exception=True)
        group = group_serializer.save()

        return CreateGroupMutation(group=group)


class Mutation(graphene.ObjectType):
    create_group = CreateGroupMutation.Field()
