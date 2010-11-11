from sqlalchemy import Column,ForeignKey
from sqlalchemy.types import Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, backref

from repoman.model.meta import Base
from repoman.model.associations import user_group_association
from repoman.model.certificate import Certificate
from repoman.model.quota import Quota


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)

    user_name = Column(String(100), unique=True)    # unique user name
    email = Column(String(100), unique=True)        # unique email address
    full_name = Column(String(256), default='')     # full name of user
    password = Column(String(100), default='')      # password of user

    created = Column(DateTime(), default=None)                    # GMT
    expires = Column(DateTime(), default=None)                    # GMT

    # flags
    suspended = Column(Boolean(), default=False)    # is the account suspended?
    deleted = Column(Boolean(), default=False)      # is the account deleted?

    # user certificate ref
    certificate_id = Column(Integer, ForeignKey('certificate.id'))
    certificate = relationship("Certificate", backref=backref("user", uselist=False))

    # user quota ref
    quota_id = Column(Integer, ForeignKey('quota.id'))
    quota = relationship("Quota", backref=backref("user", uselist=False))

    # list of images
    images = relationship("Image", backref="owner")

    # list of group membership
    groups = relationship("Group", secondary='user_group_association', backref="users")

    def __init__(self, user_name, email, cert_dn):
        self.user_name = user_name
        self.email = email
        self.certificate = Certificate(cert_dn)
        self.quota = Quota()

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.user_name, self.email)

