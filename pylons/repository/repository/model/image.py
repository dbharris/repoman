from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.orm import relationship, backref

from repository.model.meta import Base

class Image(Base):
    __tablename__ = "repo_images"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    #version = Column(String(10), default='1')

    # owner ref
    owner_id = Column(Integer, ForeignKey('repo_users.id'))

    # set images group membership
    group_id = Column(Integer, ForeignKey('repo_groups.id'))
    # backref to allow for group --> images lookup
    group = relationship("Group", backref=backref('repo_images', uselist=False))

    # Permissions
    owner_r = Column(Boolean(), default=True)
    owner_w = Column(Boolean(), default=True)
    group_r = Column(Boolean(), default=False)
    group_w = Column(Boolean(), default=False)
    other_r = Column(Boolean(), default=False)
    other_w = Column(Boolean(), default=False)
    # Other Stuff
    desc = Column(String(256), default='')      # Human readable description
    path = Column(String(256), default='')      # path to file
    meta = Column(String(256), default='')      # path to metadata file


    def __repr__(self):
        return "<Image('%s', '%s')>" % (self.name, self.owner_id)