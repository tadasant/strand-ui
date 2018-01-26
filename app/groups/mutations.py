import graphene

from app.api.authorization import check_authorization
from app.groups.validators import GroupValidator
from app.groups.types import GroupType, GroupInputType


class CreateGroupMutation(graphene.Mutation):
    class Arguments:
        input = GroupInputType(required=True)

    group = graphene.Field(GroupType)

    @check_authorization
    def mutate(self, info, input):
        group_validator = GroupValidator(data=input)
        group_validator.is_valid(raise_exception=True)
        group = group_validator.save()

        return CreateGroupMutation(group=group)


class Mutation(graphene.ObjectType):
    create_group = CreateGroupMutation.Field()
