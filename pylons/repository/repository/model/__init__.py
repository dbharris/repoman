"""The application's model objects"""
from repository.model.meta import Session, Base

from repository.model.user import User
from repository.model.group import Group
from repository.model.image import Image, ImageShare
from repository.model.permission import Permission
from repository.model.quota import Quota
from repository.model.checksum import Checksum
from repository.model.certificate import Certificate


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)

