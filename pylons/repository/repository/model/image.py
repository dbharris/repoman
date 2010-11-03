from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship, backref

from repository.model.meta import Base


class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True)      # ID unique to the database
    uuid = Column(String(32), unique=True)      # 32-char representation

    uploaded = Column(DateTime())               # use GMT
    modified = Column(DateTime())               # use GMT
    version = Column(Integer, default=1)
    size = Column(Integer)
    checksum_id = Column(Integer, ForeignKey('checksum.id'))
    checksum = relationship("Checksum", backref=backref("image", uselist=False))

    name = Column(String(256))                  # name of image
    desc = Column(String(256), default='')      # Human readable description

    os_variant = Column(String(100))            # sl55, debian, etc
    os_type = Column(String(100))
    os_arch = Column(String(100))
    hypervisor = Column(String(100))

    url = Column(String(256))                   # Current url for the image

    # owner ref
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship("User", backref=backref('image', uselist=False))


    # Permissions
    owner_r = Column(Boolean(), default=True)
    owner_w = Column(Boolean(), default=True)
    group_r = Column(Boolean(), default=False)
    other_r = Column(Boolean(), default=False)
    # Other Stuff

    raw_uploaded = Column(Boolean(), default=False)     #
    path = Column(String(256), default='')              # path to file



    def __repr__(self):
        return "<Image('%s', '%s')>" % (self.name, self.owner_id)

