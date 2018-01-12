import pytest
from django.db.utils import IntegrityError


class TestUserModel():
    """Test potential exceptions for User model."""

    @pytest.mark.django_db
    def test_email_is_null(self, user_factory):
        """
        Given: The database has been created.
        When: A user is created without an email.
        Then: No constraint is violated.
        """
        user = user_factory(email=None)
        assert user.email is None

    @pytest.mark.django_db
    def test_email_is_unique(self, user_factory):
        """
        Given: The database contains a user with email address X.
        When: A new user is created also with email address X.
        Then: A unique constraint is violated.
        """
        user = user_factory(email='hello@gmail.com')
        with pytest.raises(IntegrityError):
            another_user = user_factory(email='hello@gmail.com')