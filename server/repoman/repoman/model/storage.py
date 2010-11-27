# Unused currently

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship, backref

from repoman.model.meta import Base

class ImageStorage(Base):
    __tablename__ = 'image_storage'

    id = Column(Integer, primary_key=True)

    storage_type = Column(String(50))
    remote_host = Column(String(256), default='')
    remote_port = Column(Integer)
    remote_user = Column(String(256))
    key = Column(String(256))

