from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from database.base import Base
from database.mixins.base import BaseMixin


class User(Base, BaseMixin):

    user_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)

    # Relation
    role = relationship(
        "Role", secondary="user_role", back_populates="user", lazy=True, uselist=False
    )
