from __future__ import annotations

import bcrypt

from api.models import Base
from api.models import byt_60
from api.models import orm
from api.models import str_100


class User(Base):
    """
    Application user.
    """

    email: orm.Mapped[str_100] = orm.mapped_column(unique=True)
    pwhash: orm.Mapped[byt_60]

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.pwhash = User.hashpw(password)

    def __repr__(self: User) -> str:
        """
        ** Overrides `Base` **

        Do not show password hash.

        Example:
        ```
        >>> User(email="foo@bar.com", password="correct-horse-battery-staple")
        >>> <User id=1, email='foo@bar.com'>
        ```
        """
        return f"<User id={self.id}, email={self.email!r}>"

    @staticmethod
    def hashpw(password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def checkpw(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.pwhash)
