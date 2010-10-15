# NOT CURRENTLY USED

from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.orm import relationship, backref

from repository.model.meta import Base
from repository.model.user_group_association import ug_association_table


class UserType(Base):
    __tablename__ = "repo_user_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)


    users = relationship("User",
                          secondary=ug_association_table,
                          backref="repo_user_types"
                         )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<UserType('%s')>" % (self.name)