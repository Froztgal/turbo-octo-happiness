from django.db.models import Model, QuerySet
from pydantic import BaseModel


def one_to_pydantic(model: Model, schema: BaseModel):
    return schema.parse_obj(model.__dict__)


def many_to_pydantic(query_set: QuerySet, schema: BaseModel):
    result = []
    for obj in query_set:
        if isinstance(obj, dict):
            result.append(schema.parse_obj(obj))
        else:
            result.append(schema.parse_obj(obj.__dict__))
    return result
