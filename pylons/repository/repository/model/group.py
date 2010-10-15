from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.orm import relationship, backref

from repository.model.meta import Base

class Group(Base):
    __tablename__ = "repo_groups"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(32), unique=True)
    name = Column(String(100), unique=True)

    # one --> many realation
    #admins = relationship("User", backref="repo_groups")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Group('%s')>" % (self.name)
