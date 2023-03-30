from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select

from database.base import get_session


async def db_select(query: Select, session: AsyncSession = get_session()):
    result = await session.execute(query)
    result_list = result.scalars().all()
    if len(result_list) == 0:
        return None
    elif len(result_list) == 1:
        return result_list[0]
    else:
        return result_list
