import graphene

from app.users.models import User
from app.users.types import UserInputType, UserType


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        input = UserInputType(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            raise Exception('Unauthorized')

        user = User.objects.create(**input)
        return CreateUserMutation(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
