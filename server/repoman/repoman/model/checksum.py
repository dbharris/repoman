from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.orm import relationship, backref

from repoman.model.meta import Base


class Checksum(Base):
    __tablename__ = "checksum"

    id = Column(Integer, primary_key=True)

    ctype = Column(String(32))
    cvalue = Column(String(128))

