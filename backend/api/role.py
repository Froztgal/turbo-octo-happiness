from fastapi import APIRouter, Depends

from database.models.role import Role
from sqlalchemy.ext.asyncio import AsyncSession
from database.base import get_session

router = APIRouter(prefix="/role", tags=["Role"])

@router.post("/")
async def register_user(fields: dict, 
                        session: AsyncSession = Depends(get_session)):
    obj = fields
    session.add(Role(**fields))
    await session.commit()
    await session.refresh(obj)
    return obj