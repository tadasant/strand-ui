import graphene

from app.groups.models import Group
from app.groups.types import GroupType


class Query(graphene.ObjectType):
    group = graphene.Field(GroupType, id=graphene.Int(), name=graphene.String())
    groups = graphene.List(GroupType)

    def resolve_group(self, info, id=None, name=None):
        if id is not None:
            return Group.objects.get(pk=id)

        if name is not None:
            return Group.objects.get(name=name)

        return None

    def resolve_groups(self, info):
        return Group.objects.all()
