import pytest
from django.db.utils import IntegrityError

from app.users.models import User
from tests.factories import UserFactory


class TestUserModel():
    """Test potential exceptions for User model."""

    @pytest.mark.django_db
    def test_email_is_null(self):
        """
        Given: The database has been created.
        When: A user is created without an email.
        Then: No constraint is violated.
        """
        user_factory = UserFactory(email=None)
        user_factory.save()
        assert user_factory.email is None

    @pytest.mark.django_db
    def test_email_is_unique(self):
        """
        Given: The database contains a user with email address X.
        When: A new user is created also with email address X.
        Then: A unique constraint is violated.
        """
        User.objects.create(email='hello@gmail.com')
        with pytest.raises(IntegrityError):
            User.objects.create(email='hello@gmail.com')