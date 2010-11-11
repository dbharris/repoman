"""The application's model objects"""
from repoman.model.meta import Session, Base

from repoman.model.user import User
from repoman.model.group import Group
from repoman.model.image import Image, ImageShare
from repoman.model.permission import Permission
from repoman.model.quota import Quota
from repoman.model.checksum import Checksum
from repoman.model.certificate import Certificate

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)

