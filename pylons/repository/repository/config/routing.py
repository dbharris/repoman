"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE

    map.resource('whoami', 'whoami', controller='api/whoami',
                  path_prefix='/api', name_prefix='api_')

    map.resource('user', 'users', controller='api/users',
                 path_prefix='/api', name_prefix='api_')

    map.resource('group', 'groups', controller='api/groups',
                 path_prefix='/api', name_prefix='api_')

    map.resource('meta', 'meta', controller='api/images/meta',
                  path_prefix='/api/images', name_prefix='api_images_')

    # Manually set the routing for images/raw.
    map.connect('/api/images/raw/:(id)', controller='api/images/raw',
                 action='post_upload', conditions=dict(method=['POST']))
    map.connect('/api/images/raw/:id', controller='api/images/raw',
                 action='put_upload', conditions=dict(method=['PUT']))
    map.connect('/api/images/raw/:id', controller='api/images/raw',
                 action='show', conditions=dict(method=['GET']))


    # End of custom routes

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map

