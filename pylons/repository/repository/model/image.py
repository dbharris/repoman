from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship, backref

from repository.model.meta import Base


class Image(Base):
    __tablename__ = "repo_images"

    id = Column(Integer, primary_key=True)      # ID unique to the database
    uuid = Column(String(32), unique=True)      # 32-char representation
    version = Column(Integer, default=1)        #
    uploaded = Column(DateTime())               # use GMT
    modified = Column(DateTime())               # use GMT

    name = Column(String(100))                  # name of image
    checksum = Column(String(32))               # MD5?
    os_variant = Column(String(100))            # sl55, debian, etc
    os_type = Column(String(100))
    os_arch = Column(String(100))
    hypervisor = Column(String(100))

    url = Column(String(256))                   # Current url for the image
    previous = Column(String(256), default='')

    # owner ref
    owner_id = Column(Integer, ForeignKey('repo_users.id'))
    owner = relationship("User", backref=backref('repo_images', uselist=False))

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


    def __repr__(self):
        return "<Image('%s', '%s')>" % (self.name, self.owner_id)