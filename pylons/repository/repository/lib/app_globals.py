"""The application's Globals object"""

from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from pylons import config

from uuid import UUID


class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self, config):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        self.cache = CacheManager(**parse_cache_config_options(config))

        # Repository Stuff
        self.UUID_NAMESPACE = UUID(config['global_conf']['uuid_namespace'])

        self.image_storage = config['global_conf']['image_storage']