import graphene
import app.groups.mutations
import app.groups.queries
import app.slack.mutations
import app.slack.queries
import app.users.mutations
import app.users.queries
import app.questions.schema
import app.messages.schema


# TODO: Migrate each app's Query objects to queries.py as Mutations are added
class Query(app.groups.queries.Query, app.messages.schema.Query,
            app.questions.schema.Query, app.slack.queries.Query,
            app.users.queries.Query, graphene.ObjectType):
    pass


class Mutation(app.groups.mutations.Mutation, app.slack.mutations.Mutation,
               app.users.mutations.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
