from uuid import uuid4

from django.db.models import CharField, DateTimeField, Model, UUIDField
from pydantic import BaseModel


class BaseMixin(Model):
    id = UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

    def to_pydantic(self, schema: BaseModel) -> BaseModel:
        return schema.parse_obj(self.__dict__)


class BaseTimestampMixin(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseUserTrackMixin(Model):
    created_by = CharField()
    updated_by = CharField()

    class Meta:
        abstract = True


class AuditMixin(BaseTimestampMixin, BaseUserTrackMixin):
    class Meta:
        abstract = True
