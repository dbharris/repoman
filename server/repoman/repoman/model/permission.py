from sqlalchemy import Column,ForeignKey
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.orm import relationship, backref

from repoman.model.meta import Base
from repoman.model.associations import group_permission_association
from repoman.model.group import Group


class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True)

    permission_name = Column(String(32), unique=True)
    groups = relationship("Group", secondary="group_permission_association", backref='permissions')

    def __init__(self, permission_name):
        self.permission_name = permission_name

    def __repr__(self):
        return "<Permission('%s')>" % self.permission_name

