from pydantic import BaseModel
from typing import (
    Generic,
    Type,
    TypeVar,
    List
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import (
    update as sql_update,
    delete as sql_delete,
)

T = TypeVar("T")
PType = TypeVar('PType', bound=BaseModel)

class BaseSqlAlchemyRepository(Generic[T, PType]):

    def __init__(self, model: Type[T], pydantic_model: Type[PType], session: AsyncSession):
        self.model = model
        self.pydantic_model = pydantic_model
        self.session = session

    async def get(self, pk: int) -> PType:
        stmt = select(self.model).where(self.model.id == pk)
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()
        if not instance:
            raise ValueError
        return self.pydantic_model.model_validate(instance, from_attributes=True)

    async def create(self, instance_data: PType) -> PType:
        instance = self.model(**instance_data.model_dump())
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return self.pydantic_model.model_validate(instance, from_attributes=True)

    async def update(self, pk: int, update_data: PType) -> PType:
        await self.session.execute(
            sql_update(self.model).where(self.model.id == pk).values(**update_data.model_dump())
        )
        await self.session.commit()
        return await self.get(pk=pk)


    async def delete(self, pk: int) -> None:
        await self.session.execute(sql_delete(self.model).where(self.model.id == pk))
        await self.session.commit()


    async def all(self) -> List[PType]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        instances = result.scalar().all()
        return [
            self.pydantic_model.model_validate(instance, from_attributes=True)
            for instance in instances
        ]

    async def filter(self, **kwargs) -> List[PType]:
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        instances = result.scalar().all()
        return [
            self.pydantic_model.model_validate(instance, from_attributes=True)
            for instance in instances
        ]

