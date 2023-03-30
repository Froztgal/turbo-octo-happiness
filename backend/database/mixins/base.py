from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID


class BaseMixin(object):
    
    id =  Column(UUID, primary_key=True, default=str(uuid4()))