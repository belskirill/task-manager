from pydantic import BaseModel

from src.database import Base
from src.repositories.mappers.base import DataMapper
from sqlalchemy import insert


class BaseRepository:
    model: type[Base]
    mapper: type[DataMapper]


    def __init__(self, session):
        self.session = session


    async def add_data(self, data: BaseModel):
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
        )

        await self.session.execute(stmt)