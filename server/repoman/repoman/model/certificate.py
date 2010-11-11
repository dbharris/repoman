from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.orm import relationship, backref

from repoman.model.meta import Base


class Certificate(Base):
    __tablename__ = "certificate"

    id = Column(Integer, primary_key=True)

    # Client
    client_dn = Column(String(256), unique=True)
    # Issuer
    issuer_dn = Column(String(256), default='')

    def __init__(self, client_dn, issuer_dn=None):
        self.client_dn = client_dn
        self.issuer_dn = issuer_dn

    def __repr__(self):
        return "<Certificate('%s')>" % self.client_dn

