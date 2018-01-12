from collections import OrderedDict

import graphene
import pytest

from app.users.schema import Query as UserQuery


class TestUserQuery():
    """Test user API queries"""

    @pytest.mark.django_db
    def test_get_user(self, user_factory):
        user = user_factory()
        user.save()

        schema = graphene.Schema(query=UserQuery)
        query = '''
            query {
              user(id: %s) {
                firstName
              }
            }
        ''' % user.id
        result = schema.execute(query)
        assert not result.errors
        assert result.data == {
            'user': OrderedDict([('firstName', user.first_name)])
        }

    @pytest.mark.django_db
    def test_get_users(self, user_factory):
        user = user_factory()
        user.save()

        second_user = user_factory()
        second_user.save()

        schema = graphene.Schema(query=UserQuery)
        query = '''
            query {
               users {
                  username
               }
            }
        '''
        result = schema.execute(query)
        assert not result.errors
        assert len(result.data['users']) == 2
