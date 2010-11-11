from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, backref

from repoman.model.meta import Base

class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    created = Column(DateTime())
    protected = Column(Boolean, default=False)
    name = Column(String(100), unique=True)

    #Permissions are linked to groups from within the Permissions object
    #Permissions will be available here by the 'permissions' backref

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Group('%s')>" % (self.name)

