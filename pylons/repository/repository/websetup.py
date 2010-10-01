"""Setup the repository application"""
import logging

import pylons.test

from repository.config.environment import load_environment
from repository.model.meta import Session, Base

from repository import model

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup repository here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    Base.metadata.create_all(bind=Session.bind)

    # Default groups
    users = model.Group(name='users')
    Session.add(users)
    Session.commit()

    # Me, TAKE ME OUT!!!
    user = model.User(name='Matt Vliet', email="mvliet@uvic.ca",
                      client_dn='/C=CA/O=Grid/OU=phys.uvic.ca/CN=Matt Vliet')
    user.global_admin=True
    user.groups.append(users)
    Session.add(user)
    
    user = model.User(name='Kyle Fransham', email="fransham@uvic.ca",
                      client_dn='/C=CA/O=Grid/OU=uvic.ca/CN=Kyle Fransham')
    user.global_admin=True
    user.groups.append(users)


    Session.commit()
