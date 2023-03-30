from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import column_property, relationship

from database.base import Base
from database.mixins.base import BaseMixin


class UserInfo(Base, BaseMixin):

    first_name = Column(String)
    last_name = Column(String)
    avatar = Column(String)
    phone_number = Column(String)

    # Relation
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="user_info", 
                        lazy=True, uselist=False)

    # Property
    fullname = column_property(f"{first_name} {last_name}")
