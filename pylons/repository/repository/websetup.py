"""Setup the repository application"""
import logging

import pylons.test

from repository.config.environment import load_environment
from repository.model.meta import Session, Base

from repository import model
import uuid

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup repository here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    Base.metadata.create_all(bind=Session.bind)

    namespace = uuid.UUID(conf.global_conf['uuid_namespace'])

    # Default groups
    users = model.Group(name='users')
    users.uuid = uuid.uuid3(namespace, 'GROUP'+'users').hex
    Session.add(users)
    Session.commit()


