import importlib
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.future import select

from database.base import get_session


def generate(
        database_model: DeclarativeMeta,
        response_models_module: str
        ):
    
    # Load response models
    response_models_dict = {"Get": None, "Post": None, "Update": None}

    module = importlib.import_module(response_models_module)
    
    for method in response_models_dict.keys():
        model = getattr(module, f"{database_model.__name__}{method}", None)
        if model is not None:
            response_models_dict[method] = model

    # Create router
    router = APIRouter(
        prefix=f"/{database_model.__name__.lower()}", 
        tags=[database_model.__name__]
    )

    # Add get method
    @router.get("/{id}", response_model=response_models_dict["Get"])
    async def get(id: UUID, session: AsyncSession = Depends(get_session)):
        return await session.get(database_model, str(id))
    
    # Add post method
    @router.post("/", response_model=response_models_dict["Get"])
    async def post(fields: response_models_dict["Post"], 
                   session: AsyncSession = Depends(get_session)):
        obj = database_model(**fields.__dict__)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
    
    @router.post("/{id}", response_model=response_models_dict["Get"])
    async def update(id: UUID, fields: response_models_dict["Update"], 
                     session: AsyncSession = Depends(get_session)):
        obj = await session.get(database_model, str(id))
        for k, v in fields.items():
            if hasattr(obj, k) and getattr(obj, k) != v:
                setattr(obj, k, v)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
    
    @router.delete("/{id}", response_model=response_models_dict["Get"])
    async def delete(id: UUID, session: AsyncSession = Depends(get_session)):
        obj = await session.get(database_model, str(id))
        await session.delete(obj)
        await session.commit()
        return obj
    
    # Get all
    @router.get("/", response_model=list[response_models_dict["Get"]])
    async def get_may(page_size: int = 20, page: int = 0, 
                  session: AsyncSession = Depends(get_session)):
        query = select(database_model).offset(page*page_size).limit(page_size)
        result = await session.execute(query)
        return result.scalars().all()

    return router
