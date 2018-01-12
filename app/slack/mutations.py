import graphene
from app.slack.types import SlackUserType, SlackUserInputType
from app.slack.models import SlackTeam, SlackUser
from app.users.models import User


class CreateSlackUserMutation(graphene.Mutation):
    class Arguments:
        input = SlackUserInputType(required=True)

    status = graphene.Int()
    form_errors = graphene.String()
    slack_user = graphene.Field(lambda: SlackUserType)

    def mutate(self, info, input):
        if not info.context.user.is_authenticated:
            return CreateSlackUserMutation(status=403)

        if not SlackTeam.objects.filter(pk=input.slack_team_id).exists():
            return CreateSlackUserMutation(status=400,
                                           form_errors={'message': ['Invalid Slack Team Id']})
        if not User.objects.filter(pk=input.user_id).exists():
            return CreateSlackUserMutation(status=400,
                                           form_errors={'message': ['Invalid User Id']})

        slack_user = SlackUser.objects.create(**input)
        return CreateSlackUserMutation(slack_user=slack_user)


class Mutation(graphene.ObjectType):
    create_slack_user = CreateSlackUserMutation.Field()
