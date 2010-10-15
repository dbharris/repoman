"""The application's model objects"""
from repository.model.meta import Session, Base

from repository.model.user import User
#from repository.model.user_types import UserType
from repository.model.group import Group
from repository.model.image import Image


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)
