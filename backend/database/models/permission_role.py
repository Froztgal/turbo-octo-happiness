from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from database.base import Base


class PermissionRole(Base):

    role_id =  Column(UUID, ForeignKey('role.id'), 
                      primary_key=True, nullable=False)

    permission_id =  Column(UUID, ForeignKey('permission.id'), 
                      primary_key=True, nullable=False)
    