from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from database.base import Base


class UserRole(Base):

    user_id =  Column(UUID, ForeignKey('user.id'), 
                      primary_key=True, nullable=False)
    role_id =  Column(UUID, ForeignKey('role.id'), 
                      primary_key=True, nullable=False)
