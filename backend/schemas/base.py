from enum import Enum
from typing import Any

from pydantic import BaseModel


class Method(str, Enum):
    eq = "eq"
    gt = "gt"
    lt = "lt"
    gte = "gte"
    lte = "lte"
    ne = "ne"
    like = "like"
    between = "between"
    # "in" is a python keyword
    into = "in"


class Filter(BaseModel):
    field: str
    method: Method
    value: Any


class Direction(str, Enum):
    asc = "asc"
    desc = "desc"


class Order(BaseModel):
    field: str
    direction: Direction


class CommonQuery(BaseModel):
    page_number: int
    page_size: int
    filters: list[Filter]
    orders: list[Order]
    included: list[str]
    excluded: list[str]
