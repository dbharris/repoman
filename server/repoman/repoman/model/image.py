from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship, backref

from repoman.model.meta import Base
from repoman.model.associations import imageshare_user_association
from repoman.model.associations import imageshare_group_association
from repoman.model.checksum import Checksum

class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True)      # ID unique to the database
    uuid = Column(String(64), unique=True)      # 32-char representation

    uploaded = Column(DateTime())               # use GMT
    modified = Column(DateTime())               # use GMT
    expires = Column(DateTime())                # use GMT
    version = Column(Integer, default=0)        # incrimented on new upload
    size = Column(Integer)                      # bytes

    name = Column(String(256))                  # name of image
    description = Column(String(256))           # Human description

    os_variant = Column(String(100))            # sl55, debian, etc
    os_type = Column(String(100))               # linux, windows, unix, etc.
    os_arch = Column(String(100))               # x86, x86_64
    hypervisor = Column(String(100))            # xen, kvm, etc.

    path = Column(String(256), default='')      # path to file

    # flags
    deleted = Column(Boolean(), default=False)          # image deleted?
    read_only = Column(Boolean(), default=False)        # protect from overwrite
    raw_uploaded = Column(Boolean(), default=False)     # has it been uploaded?
    unauthenticated_access = Column(Boolean(), default=False)   # gettable from http?

    # Adjacency list relationship
    # track what images were based on what images
    #  parent_image - the image this image is based from
    #  child_images - list of images based off this image
    parent_image_id = Column(Integer, ForeignKey('image.id'))
    child_images = relationship("Image", backref=backref("parent_image", remote_side=id))

    # checksum ref
    checksum_id = Column(Integer, ForeignKey('checksum.id'))
    checksum = relationship("Checksum", backref=backref("image", uselist=False))

    # owner ref
    owner_id = Column(Integer, ForeignKey('user.id'))
    #owner = relationship("User", backref=backref('image', uselist=False))

    # sharing ref
    shared_id = Column(Integer, ForeignKey('image_share.id'))
    shared = relationship("ImageShare", backref=backref("image", uselist=False))

    def __repr__(self):
        return "<Image('%s', '%s')>" % (self.name, self.owner.user_name)

    def __init__(self):
        self.checksum = Checksum()
        self.shared = ImageShare()




class ImageShare(Base):
    __tablename__ = "image_share"

    id = Column(Integer, primary_key=True)
    enabled = Column(Boolean, default=True)

    # One-to-many relationship (ImageShare<->User(s))
    users = relationship("User", secondary='imageshare_user_association',
                         backref='shared_images')

    # One-to-many relationship (ImageShare<->Groups(s))
    groups = relationship("Group", secondary='imageshare_group_association',
                          backref='shared_images')

