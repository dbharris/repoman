"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from pylons import app_globals
from uuid import uuid3

###
true_values = (True, 'true', '1')
def str_to_bool(value):
    if value.lower() in true_values:
        return True
    else:
        return False


###
def user_uuid(client_dn):
    return uuid3(app_globals.UUID_NAMESPACE, str(client_dn)).hex

def group_uuid(name):
    return uuid3(app_globals.UUID_NAMESPACE, 'GROUP'+str(name)).hex

def image_uuid(client_dn, image_name):
    """order of params matters!  when in doubt name the params."""
    return uuid3(app_globals.UUID_NAMESPACE, str(client_dn)+str(image_name)).hex
