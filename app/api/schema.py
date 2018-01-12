import graphene
import app.users.schema
import app.groups.schema
import app.slack.queries
import app.slack.mutations
import app.questions.schema
import app.messages.schema


class Query(app.users.schema.Query, app.groups.schema.Query,
            app.slack.queries.Query, app.questions.schema.Query,
            app.messages.schema.Query, graphene.ObjectType):
    pass


class Mutation(app.slack.mutations.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
