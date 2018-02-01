import graphene

import app.groups.mutations
import app.groups.queries
import app.discussions.mutations
import app.discussions.queries
import app.topics.mutations
import app.topics.queries
import app.slack_integration.mutations
import app.slack_integration.queries
import app.users.mutations
import app.users.queries


class Query(app.groups.queries.Query, app.discussions.queries.Query,
            app.topics.queries.Query, app.slack_integration.queries.Query,
            app.users.queries.Query, graphene.ObjectType):
    pass


class Mutation(app.groups.mutations.Mutation, app.discussions.mutations.Mutation,
               app.topics.mutations.Mutation, app.slack_integration.mutations.Mutation,
               app.users.mutations.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
