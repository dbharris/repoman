from sqlalchemy import Column,ForeignKey
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.orm import relationship, backref

from repository.model.meta import Base
from repository.model.associations import user_group_association
from repository.model.certificate import Certificate


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)

    # User info type stuff
    user_name = Column(String(100), unique=True)
    password = Column(String(100))
    full_name = Column(String(100), default='')
    email = Column(String(100), default='')

    # admin type stuff
    suspended = Column(Boolean(), default=False)
    deleted = Column(Boolean(), default=False)

    # relationships
    certificate_id = Column(Integer, ForeignKey('certificate.id'))
    certificate = relationship("Certificate", backref=backref("user", uselist=False))
    quota_id = Column(Integer, ForeignKey('quota.id'))
    quota = relationship("Quota", backref=backref("user", uselist=False))
    images = relationship("Image", backref="user")
    groups = relationship("Group", secondary='user_group_association', backref="users")

    def __init__(self, user_name, email, cert_dn):
        self.user_name = user_name
        self.email = email
        self.certificate = Certificate(cert_dn)

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.user_name, self.email)

