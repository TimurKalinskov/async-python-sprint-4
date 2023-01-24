from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, AnyUrl


class UrlBase(BaseModel):
    url: HttpUrl


class ShortUrlCreate(UrlBase):
    url_short: Optional[AnyUrl] = None


class ShortUrlUpdate(UrlBase):
    pass


class ShortUrlInDBBase(UrlBase):
    id: int
    url: HttpUrl
    url_short: AnyUrl
    created_at: datetime

    class Config:
        orm_mode = True


class ShortUrl(ShortUrlInDBBase):
    pass
