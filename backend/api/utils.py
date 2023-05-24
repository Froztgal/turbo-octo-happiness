from django.db.models import Model, Q, QuerySet
from fastapi import Query

from schemas.base import CommonQuery, Filter, Order


def get_common_query(
    page_number: int = 0,
    page_size: int = 20,
    filter: list[str] = Query(default=[]),
    order: list[str] = Query(default=[]),
    included: list[str] = Query(default=[]),
    excluded: list[str] = Query(default=[]),
) -> CommonQuery:
    filters: list[Filter] = []
    orders: list[Order] = []

    for f in filter:
        field, method, value = f.split(".")
        filters.append(Filter(field=field, method=method, value=value))

    for o in order:
        field, direction = o.split(".")
        orders.append(Order(field=field, direction=direction))

    return CommonQuery(
        page_number=page_number,
        page_size=page_size,
        filters=filters,
        orders=orders,
        included=included,
        excluded=excluded,
    )


def filter_model(model: Model, params: CommonQuery) -> QuerySet:
    # Filters
    query = Q()
    for filter in params.filters:
        match filter.method:
            case "eq":
                query |= Q(**{filter.field: filter.value})
            case _:
                match filter.method:
                    case "like":
                        method = "icontains"
                    case "between":
                        method = "range"
                    case _:
                        method = filter.method
                query |= Q(**{f"{filter.field}__{method}": filter.value})

    # Ordering
    ordering = []
    for order in params.orders:
        sign = "-" if order.direction == "desc" else ""
        ordering.append(f"{sign}{order.field}")

    # Final QuerySet
    result: QuerySet = model.objects.filter(query)
    if ordering:
        result = result.order_by(ordering)
    if params.included:
        result = result.values(*params.included)
    # Can't exclude id field
    elif params.excluded:
        result = result.defer(*params.excluded)

    start = params.page_number * params.page_size
    stop = start + params.page_size
    return result[start:stop]
