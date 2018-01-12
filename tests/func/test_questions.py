import graphene
import pytest

from app.questions.schema import Query


class TestQuestionQuery():
    """Test question API queries"""

    @pytest.mark.django_db
    def test_get_question(self, question_factory):
        question = question_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
              question(id: %s) {
                title
              }
            }
        ''' % question.id
        result = schema.execute(query)
        assert not result.errors
        assert result.data['question']['title'] == question.title

    @pytest.mark.django_db
    def test_get_questions(self, question_factory):
        question = question_factory()
        another_question = question_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
               questions {
                  title
               }
            }
        '''
        result = schema.execute(query)
        assert not result.errors
        assert len(result.data['questions']) == 2


class TestTagQuery():
    """Test tag API queries"""

    @pytest.mark.django_db
    def test_get_tag(self, tag_factory):
        tag = tag_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
              tag(name: "%s") {
                id
              }
            }
        ''' % tag.name
        result = schema.execute(query)
        assert not result.errors
        assert int(result.data['tag']['id']) == tag.id

    @pytest.mark.django_db
    def test_get_tags(self, tag_factory):
        tag = tag_factory()
        another_tag = tag_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
              tags {
                name
              }
            }
        '''
        result = schema.execute(query)
        assert not result.errors
        assert len(result.data['tags']) == 2


class TestSessionQuery():
    """Test session API queries"""

    @pytest.mark.django_db
    def test_get_session(self, session_factory):
        session = session_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
              session(id: %s) {
                question {
                  title
                }
              }
            }
        ''' % session.id
        result = schema.execute(query)
        assert not result.errors
        assert result.data['session']['question']['title'] == session.question.title


    @pytest.mark.django_db
    def test_get_sessions(self, session_factory):
        session = session_factory()
        another_session = session_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
              sessions {
                id
              }
            }
        '''
        result = schema.execute(query)
        assert not result.errors
        assert len(result.data['sessions']) == 2
