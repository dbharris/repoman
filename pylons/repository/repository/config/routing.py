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
    ####################

    # TODO:mvliet: name the routes

    # Whoami
    map.connect(None, '/api/whoami', controller='api/whoami', action='whoami',
                conditions=dict(method=['GET']))

    # User Routes
    map.connect(None, '/api/users', controller='api/users', action='list_all',
                conditions=dict(method=['GET']))

    map.connect(None, '/api/users', controller='api/users', action='new_user',
                conditions=dict(method=['POST']))

    map.connect(None, '/api/users/:(user)', controller='api/users', action='show',
                conditions=dict(method=['GET']))

    map.connect(None, '/api/users/:(user)/images', controller='api/users',
                action='list_images',
                conditions=dict(method=['GET']))

    map.connect(None, '/api/users/:(user)/groups', controller='api/users',
                actions='list_groups',
                conditions=dict(method=['GET']))

    map.connect(None, '/api/users/:(user)/permissions', controller='api/users',
                action='list_permissions',
                conditions=dict(method=['GET']))

    map.connect(None, '/api/users/:(user)/shared_images', controller='api/users',
                action='list_shared_images',
                conditions=dict(method=['GET']))

    # Group Routes
    map.connect(None, '/api/groups', controller='api/groups', action='list_all',
                conditions=dict(method=['GET']))

    map.connect(None, '/api/groups', controller='api/groups', action='new_group',
                conditions=dict(method=['POST']))

    map.connect(None, '/api/groups/:(group)', controller='api/groups', action='show',
                conditions=dict(method=['GET']))

    map.connect(None, '/api/groups/:(group)/users', controller='api/groups',
                action='list_users',
                conditions=dict(method=['GET']))

    map.connect(None, '/api/groups/:(group)/users/:(user)', controller='api/groups',
                action='add_user',
                conditions=dict(method=['POST']))

    map.connect(None, '/api/groups/:(group)/users/:(user)', controller='api/groups',
                action='remove_user',
                conditions=dict(method=['DELETE']))

    map.connect(None, '/api/groups/:(group)/permissions', controller='api/groups',
                action='list_permissions',
                conditions=dict(method=['GET']))

    map.connect(None, '/api/groups/:(group)/permissions/:(permission)',
                controller='api/groups',
                action='add_permission',
                conditions=dict(method=['POST']))

    map.connect(None, '/api/groups/:(group)/permissions/:(permission)',
                controller='api/groups',
                action='remove_permission',
                conditions=dict(method=['DELETE']))

    # Image Routes
    map.connect(None, '/api/images/:(user)/:(image)/raw', controller='api/images',
                action='get_raw_image',
                conditions=dict(method=['GET']))

    map.connect(None, '/api/images/:(user)/:(image)/raw', controller='api/images',
                action='upload_raw',
                conditions=dict(method=['POST']))

    map.connect(None, '/api/images/:(image)/raw', controller='api/images',
                action='get_raw_image',
                conditions=dict(method=['GET']))

    map.connect(None, '/api/images/:(image)/raw', controller='api/images',
                action='upload_raw',
                conditions=dict(method=['POST']))

    map.connect(None, '/api/images/:(user)/:(image)', controller='api/images',
                action='show_image_meta',
                conditions=dict(method=['GET']))

    map.connect(None, '/api/images/:(user)/:(image)', controller='api/images',
                action='modify_image_meta',
                conditions=dict(method=['POST']))

    map.connect(None, '/api/images/:(user)/:(image)', controller='api/images',
                action='delete_image',
                conditions=dict(method=['DELETE']))

    map.connect(None, '/api/images/:(image)', controller='api/images',
                action='show_image_meta',
                conditions=dict(method=['GET']))

    map.connect(None, '/api/images/:(image)', controller='api/images',
                action='modify_image_meta',
                conditions=dict(method=['POST']))

    map.connect(None, '/api/images/:(image)', controller='api/images',
                action='delete_image',
                conditions=dict(method=['DELETE']))

    map.connect(None, '/api/images', controller='api/images', action='list_all',
                conditions=dict(method=['GET']))

    map.connect(None, '/api/images', controller='api/images', action='new_image',
                conditions=dict(method=['POST']))


    # Actions
    map.connect(None, 'api/actions/clone/image/:(image)', controller='api/actions',
                action='clone_image',
                conditions=dict(method=['GET']))

    #######################
    # End of custom routes

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map

