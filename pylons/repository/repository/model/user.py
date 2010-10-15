from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.orm import relationship, backref

from repository.model.meta import Base
from repository.model.user_group_association import ug_association_table


class User(Base):
    __tablename__ = "repo_users"

    # User info type stuff
    id = Column(Integer, primary_key=True)
    uuid = Column(String(32), unique=True)
    client_dn = Column(String(100), unique=True)
    name = Column(String(100), default='')
    email = Column(String(100), default='')

    # admin type stuff
    global_admin = Column(Boolean(), default=False)
    suspended = Column(Boolean(), default=False)
    deleted = Column(Boolean(), default=False)

    # one-to-many relationship
    images = relationship("Image", backref="repo_users")

    # link user <--> group
    # many-to-many relationship
    groups = relationship("Group",
                          secondary=ug_association_table,
                          backref="repo_users"
                         )


    def __init__(self, name='', email='', client_dn=''):
        self.name = name
        self.email = email
        self.client_dn = client_dn

    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.name, self.email, self.client_dn)
