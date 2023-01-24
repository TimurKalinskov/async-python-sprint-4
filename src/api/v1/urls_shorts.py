from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from db.db import get_session
from schemas import short as short_schema
from services.short import short_crud
from services.exceptions import CreateException, UrlDeletedException
from services.short_statistic import (
    create_statistic_record, get_full_statistic, get_uses_count
)
from schemas.short_statistic import (
    ShortUrlFullStatistic, ShortUrlUsesCount, ShortUrlStatisticCreate
)


router = APIRouter()


@router.get('/', response_model=list[short_schema.ShortUrl])
async def read_short_urls(
        db: AsyncSession = Depends(get_session),
        skip: int = 0,
        limit: int = 100
) -> Any:
    """
    Retrieve list of short urls.
    """
    urls = await short_crud.get_multi(db=db, skip=skip, limit=limit)
    return urls


@router.get(
    '/{pk}',
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT
)
async def read_short_url(
        *,
        db: AsyncSession = Depends(get_session),
        pk: int,
        request: Request
) -> Any:
    """
    Get short url by ID.
    """
    try:
        short_url = await short_crud.get(db=db, pk=pk)
    except UrlDeletedException:
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail='URL deleted'
        )
    if not short_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='URL not found'
        )
    statistic_obj = ShortUrlStatisticCreate(
        url_short=short_url.url_short,
        client_host=request.client.host,
        client_port=request.client.port
    )
    await create_statistic_record(db=db, url_statistic=statistic_obj)
    return short_url.url


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=list[short_schema.ShortUrl]
)
async def create_short_url(
        *,
        db: AsyncSession = Depends(get_session),
        url_in: list[short_schema.ShortUrlCreate]
) -> Any:
    """
    Create new short url.
    """
    try:
        short_url = await short_crud.create(db=db, objects_in=url_in)
    except CreateException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Record with this url already exists'
        )
    return short_url


@router.get(
    '/{pk}/status',
    response_model=ShortUrlFullStatistic | ShortUrlUsesCount
)
async def read_short_url_statistic(
        *,
        db: AsyncSession = Depends(get_session),
        pk: int,
        full_info: bool = False,
        skip: int = 0,
        limit: int = 100
) -> Any:
    """
    Get short url statistic by ID.
    """
    try:
        if full_info:
            return await get_full_statistic(
                db=db, pk=pk, skip=skip, limit=limit
            )
        return await get_uses_count(db=db, pk=pk)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='URL not found'
        )
    except UrlDeletedException:
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail='URL deleted'
        )


@router.delete('/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_url(
    *,
    db: AsyncSession = Depends(get_session),
    pk: int
) -> None:
    """
    Delete url.
    """
    try:
        await short_crud.delete(db=db, pk=pk)
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='URL not found'
        )
