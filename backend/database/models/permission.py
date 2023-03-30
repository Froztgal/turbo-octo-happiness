from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from database.base import Base
from database.mixins.base import BaseMixin
# from database.models.permission_role import PermissionRole


class Permission(Base, BaseMixin):

    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    # Relation
    role = relationship("Role", secondary="permission_role", 
                        back_populates="permission", lazy=True, uselist=False)
