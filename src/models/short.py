from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from db.db import Base


class Short(Base):
    __tablename__ = 'url_shorts'
    id = Column(Integer, primary_key=True)
    url = Column(String(2048), unique=True, nullable=False)
    url_short = Column(String(256), unique=True, nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    deleted = Column(Boolean, default=False, nullable=False, server_default='f')

    statistics = relationship('ShortStatistic')


class ShortStatistic(Base):
    __tablename__ = 'url_statistics'
    id = Column(Integer, primary_key=True)
    url_short = Column(ForeignKey('url_shorts.url_short'))
    used_at = Column(DateTime, index=True, default=datetime.utcnow)
    client_host = Column(String(256), nullable=False)
    client_port = Column(Integer, nullable=False)

    author = relationship('Short', back_populates='statistics')
