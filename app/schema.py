import graphene
import app.users.schema
import app.groups.schema
import app.slack.schema
import app.questions.schema
import app.messages.schema


class Query(app.users.schema.Query, app.groups.schema.Query,
            app.slack.schema.Query, app.questions.schema.Query,
            app.messages.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
