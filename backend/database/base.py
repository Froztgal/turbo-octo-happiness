# import re
# from typing import AsyncGenerator

# from sqlalchemy import ChunkedIteratorResult, select, inspect
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.ext.declarative import declared_attr
# from sqlalchemy.orm import declarative_base, sessionmaker, Mapper
# from sqlalchemy.sql.selectable import Select
# from sqlalchemy.orm.attributes import InstrumentedAttribute
# from sqlalchemy.sql.elements import UnaryExpression
# from schemas.base import Filter, Order

# from config import settings
# from database.exceptions.base import (
#     NotValidAttributeForFiltering,
#     NotValidAttributeForOrdering,
# )


# class BaseClass(object):
#     @declared_attr
#     def __tablename__(cls):
#         return "_".join(re.findall("[A-Z][^A-Z]*", cls.__name__)).lower()

#     @classmethod
#     async def get(
#         cls,
#         page_number: int = 0,
#         page_size: int = 20,
#         filters: list[Filter] = [],
#         orders: list[Order] = [],
#         included: list[str] = [],
#         excluded: list[str] = [],
#     ) -> list[object] | object | None:
#         if not included and not excluded:
#             columns = [cls]
#         else:
#             inspector: Mapper = inspect(cls)
#             if included:
#                 columns = [c for c in inspector.columns if c.name in included]
#             elif excluded:
#                 columns = [c for c in inspector.columns if c.name not in excluded]

#         # Select columsn TODO fix
#         query: Select = select(*columns)

#         # Filters
#         for filter in filters:
#             # Evaluate table field from string
#             eval_field: InstrumentedAttribute = eval(".".join(("cls", filter.field)))

#             match filter.method:
#                 # Equal
#                 case "eq":
#                     query = query.filter(eval_field == filter.value)
#                 case "ne":
#                     query = query.filter(eval_field != filter.value)
#                 case "gt":
#                     query = query.filter(eval_field > filter.value)
#                 case "lt":
#                     query = query.filter(eval_field < filter.value)
#                 case "gte":
#                     query = query.filter(eval_field >= filter.value)
#                 case "lte":
#                     query = query.filter(eval_field <= filter.value)
#                 case "like":
#                     query = query.filter(eval_field.like(filter.value))
#                 case "between":
#                     query = query.filter(eval_field <= filter.value[0]).filter(
#                         eval_field >= filter.value[1]
#                     )
#                 case "in":
#                     query = query.filter(eval_field.in_(filter.value))

#         # Ordering
#         # Evaluate ordering direction from string
#         eval_orders: list[UnaryExpression] = []
#         for order in orders:
#             eval_direction: UnaryExpression = eval(
#                 ".".join(("cls", order.field, f"{order.direction}()"))
#             )
#             eval_orders.append(eval_direction)
#         query = query.order_by(*eval_orders)

#         # Limit and offset
#         query = query.offset(page_number * page_size).limit(page_size)

#         # Get result from session
#         async with async_session() as session:
#             result: ChunkedIteratorResult = await session.execute(query)
#             result_list: list[object] = result.all()
#             print(dict(result_list))
#             if len(result_list) == 0:
#                 return None
#             elif len(result_list) == 1:
#                 return result_list[0]
#             else:
#                 return result_list
