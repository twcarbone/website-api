"""
Tests for models.
"""


class TestUser:
    def test_init(self, _new_user):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check the email and pwhash fields are defined correctly
        """
        assert _new_user.email == "cheese@gmail.com"
        assert _new_user.pwhash != "my-favorite-bone"

    def test_repr(self, _new_user):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check __repr__ returns the correct representation
        """
        assert _new_user.__repr__() == "<User id=None, email='cheese@gmail.com'>"

    def test_chekpw(self, _new_user):
        """
        GIVEN a User model
        WHEN a new User is created
        THEN check that the configured password hashes to the stored database value
        """
        assert _new_user.checkpw("my-favorite-bone") == True
