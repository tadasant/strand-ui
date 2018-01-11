import graphene
import app.users.schema


class Query(app.users.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
