from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, AnyHttpUrl


class UrlBase(BaseModel):
    url: HttpUrl


class ShortUrlCreate(UrlBase):
    url_short: Optional[AnyHttpUrl] = None


class ShortUrlUpdate(UrlBase):
    pass


class ShortUrlInDBBase(UrlBase):
    id: int
    url: HttpUrl
    url_short: AnyHttpUrl
    created_at: datetime

    class Config:
        orm_mode = True


class ShortUrl(ShortUrlInDBBase):
    pass
