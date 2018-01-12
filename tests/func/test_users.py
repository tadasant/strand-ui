import graphene
import pytest

from app.users.schema import Query


class TestUserQuery():
    """Test user API queries"""

    @pytest.mark.django_db
    def test_get_user(self, user_factory):
        user = user_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
              user(id: %s) {
                firstName
              }
            }
        ''' % user.id
        result = schema.execute(query)
        assert not result.errors
        assert result.data['user']['firstName'] == user.first_name

    @pytest.mark.django_db
    def test_get_users(self, user_factory):
        user = user_factory()
        second_user = user_factory()

        schema = graphene.Schema(query=Query)
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