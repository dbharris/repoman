from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.orm import relationship, backref

from repository.model.meta import Base

class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    protected = Column(Boolean, default=False)
    name = Column(String(100), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Group('%s')>" % (self.name)

