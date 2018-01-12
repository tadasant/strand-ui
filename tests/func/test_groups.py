import graphene
import pytest

from app.groups.schema import Query


class TestGroupQuery():
    """Test group API queries"""

    @pytest.mark.django_db
    def test_get_group(self, group_factory):
        group = group_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
              group(name: "%s") {
                id
              }
            }
        ''' % group.name
        result = schema.execute(query)
        assert not result.errors
        assert int(result.data['group']['id']) == group.id

    @pytest.mark.django_db
    def test_get_groups(self, group_factory):
        group = group_factory()
        another_group = group_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
               groups {
                  name
               }
            }
        '''
        result = schema.execute(query)
        assert not result.errors
        assert len(result.data['groups']) == 2


class TestGroupSettingsQuery():
    """Test group settings API queries"""

    @pytest.mark.django_db
    def test_get_group_settings(self, group_settings_factory):
        group_settings = group_settings_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
              groupSettings(id: %s) {
                isPublic
              }
            }
        ''' % group_settings.id
        result = schema.execute(query)
        assert not result.errors
        assert int(result.data['groupSettings']['isPublic']) == group_settings.is_public

    @pytest.mark.django_db
    def test_get_groups(self, group_settings_factory):
        group_settings = group_settings_factory()
        another_group_settings = group_settings_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
               groupsSettings {
                  group {
                    name
                  }
               }
            }
        '''
        result = schema.execute(query)
        assert not result.errors
        assert len(result.data['groupsSettings']) == 2