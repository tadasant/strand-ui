import graphene

import app.groups.mutations
import app.groups.queries
import app.discussions.mutations
import app.discussions.queries
import app.questions.mutations
import app.questions.queries
import app.slack_integration.mutations
import app.slack_integration.queries
import app.users.mutations
import app.users.queries


class Query(app.groups.queries.Query, app.discussions.queries.Query,
            app.questions.queries.Query, app.slack_integration.queries.Query,
            app.users.queries.Query, graphene.ObjectType):
    pass


class Mutation(app.groups.mutations.Mutation, app.discussions.mutations.Mutation,
               app.questions.mutations.Mutation, app.slack_integration.mutations.Mutation,
               app.users.mutations.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)


class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **args):
        """
        Ensure users adhere to authorization schema through analyzing the ResolveInfo object. This object is
        updated by the GraphQL executor, as it traverses the tree. If the current operation is a mutation, we
        require authorization for all options except for createSlackAgent. For createSlackAgent, you are only
        not allowed to return the install info. If the operation is a query, we do not require authorization
        except for those that resolve SlackApplicationInstallation fields.
        """
        if not info.context.user.is_authenticated:
            if info.operation.operation == 'mutation':
                if hasattr(info.return_type, 'graphene_type') and not root:
                    # Initial resolve of a mutation
                    if info.return_type.graphene_type == schema.Mutation.create_slack_agent.type:
                        pass
                    else:
                        raise Exception('Unauthorized')
                else:
                    # Subsequent queries to mutation response
                    if hasattr(info.return_type, 'name') and \
                            info.return_type.name == 'SlackApplicationInstallationType':
                        raise Exception('Unauthorized')

            if info.operation.operation == 'query':
                if info.parent_type.name == 'SlackApplicationInstallationType':
                    raise Exception('Unauthorized')

        return next(root, info, **args)
