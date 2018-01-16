import graphene

import app.groups.mutations
import app.groups.queries
import app.messages.mutations
import app.messages.queries
import app.questions.mutations
import app.questions.queries
import app.slack.mutations
import app.slack.queries
import app.users.mutations
import app.users.queries


class Query(app.groups.queries.Query, app.messages.queries.Query,
            app.questions.queries.Query, app.slack.queries.Query,
            app.users.queries.Query, graphene.ObjectType):
    pass


class Mutation(app.groups.mutations.Mutation, app.messages.mutations.Mutation,
               app.questions.mutations.Mutation, app.slack.mutations.Mutation,
               app.users.mutations.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
