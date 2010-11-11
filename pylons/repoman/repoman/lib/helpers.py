"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from pylons import app_globals
from uuid import uuid1

import simplejson

###
true_values = (True, 'true', '1')
def str_to_bool(value):
    if value.lower() in true_values:
        return True
    else:
        return False

###
def image_uuid():
    """order of params matters!  when in doubt name the params."""
    return uuid1().hex

###
def stream_img(image_file, buff=1024):
    chunk = image_file.read(buff)
    while chunk:
        yield chunk
        chunk = image_file.read(buff)
    image_file.close()



###
def render_json(data):
    return simplejson.dumps(data)

def render_xml(data):
    pass

def render_yaml(data):
    pass

