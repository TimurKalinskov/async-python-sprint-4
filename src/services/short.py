from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound

from services.base import RepositoryDB
from services.utils import generate_short_url
from models.short import Short
from schemas.short import ShortUrlCreate, ShortUrlUpdate, ShortUrl


class RepositoryShort(RepositoryDB[Short, ShortUrlCreate, ShortUrlUpdate]):

    async def create(
            self, db: AsyncSession, *, obj_in: ShortUrlCreate) -> Short:
        if not obj_in.url_short:
            # generation of a short url and checking it not exists in the db
            short_url = generate_short_url(obj_in.url)
            statement = select(Short).where(Short.url_short == short_url)
            exist_url = await db.execute(statement=statement)
            while exist_url.scalar_one_or_none():
                short_url = generate_short_url(obj_in.url)
                exist_url = await db.execute(statement=statement)
            obj_in.url_short = short_url

        return await super().create(db=db, obj_in=obj_in)


short_crud = RepositoryShort(Short)
