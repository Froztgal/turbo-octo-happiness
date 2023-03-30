from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from database.base import Base
from database.mixins.base import BaseMixin
from database.models.permission_role import PermissionRole
from database.models.user_role import UserRole


class Role(Base, BaseMixin):

    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    # Relation
    user = relationship("User", secondary="user_role", back_populates="role", 
                        lazy=True, uselist=False)
    permission = relationship("Permission", secondary="permission_role", 
                        back_populates="role", lazy=True, uselist=False)
