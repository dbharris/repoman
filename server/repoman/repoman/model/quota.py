from sqlalchemy import Column,ForeignKey
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.orm import relationship, backref

from repoman.model.meta import Base


class Quota(Base):
    __tablename__ = "quota"

    id = Column(Integer, primary_key=True)

    max_storage = Column(Integer, default=0)
    # user
    # max_files
    # max_storage
    # max_file_size

