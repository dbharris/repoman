import formencode
import uuid

from pylons import app_globals, url, request
from pylons.controllers.util import abort, redirect

from repository.lib import helpers as h
from repository.model import meta
from repository import model

#TODO: improve abort errors by adding information to headers

#################
#   U S E R S   #
#################
def validate_new_user(params):
    schema = NewUserForm()
    try:
        result = schema.to_python(params)
    except formencode.validators.Invalid, error:
        for e,v in error.error_dict.iteritems():
            if e=='client_dn' and v.state=='CONFLICT':
                abort(409, '409 Conflict')
            else:
                abort(400, '400 Bad Request - validate_new_user')
    else:
        return result

class UniqueUsername(formencode.FancyValidator):
    """Use this class to define what makes a unique user."""
    def _to_python(self, value, state):
        user_q = meta.Session.query(model.User)
        if user_q.filter(model.User.user_name==value).first():
            state = 'CONFLICT'
        else:
            return value

class UniqueCertDN(formencode.FancyValidator):
    """Use this class to define what makes a unique user."""
    def _to_python(self, value, state):
        cert_q = meta.Session.query(model.Certificate)
        if cert_q.filter(model.Certificate.client_dn==value).first():
            state = 'CONFLICT'
            raise formencode.Invalid('conflict', value, state)
        else:
            return value

class NewUserForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    # Manditory fields here
    user_name = formencode.All(formencode.validators.String(not_empty=True),
                               UniqueUsername())
    cert_dn = formencode.All(formencode.validators.String(not_empty=True),
                             UniqueCertDN())
    email = formencode.All(formencode.validators.String(not_empty=True),
                           formencode.validators.Email())

    # Default fields here
    full_name = formencode.validators.String(not_empty=True)
    groups = formencode.validators.String(if_missing=False)
    suspended = formencode.validators.Bool(if_missing=False)


###################
#   G R O U P S   #
###################
def validate_new_group(params):
    schema = NewGroupForm()
    try:
        result = schema.to_python(params)
    except formencode.validators.Invalid, error:
        for e,v in error.error_dict.iteritems():
            if e=='name' and v.state=='CONFLICT':
                abort(409, '409 Conflict')
            else:
                abort(400, '400 Bad Request - validate_new_group')
    else:
        return result

class UniqueGroup(formencode.FancyValidator):
    """Use this class to determine the uniqueness of a group"""
    def _to_python(self, value, state):
        group_q = meta.Session.query(model.Group)
        if group_q.filter(model.Group.name==value).first():
            state = 'CONFLICT'
            raise formencode.Invalid('conflict', value, state)
        else:
            return value

class NewGroupForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    name = formencode.All(formencode.validators.String(not_empty=True),
                          UniqueGroup())
    users = formencode.validators.String(if_missing=None)


###################
#   I M A G E S   #
###################
def validate_new_image(params):
    schema = NewImageForm()
    try:
        result = schema.to_python(params)
    except formencode.validators.Invalid, error:
        for e,v in error.error_dict.iteritems():
            if e=='name' and v.state=='CONFLICT':
                abort(409, '409 Conflict')
            else:
                abort(400, '400 Bad Request - validate_new_image')
    else:
        return result

class UniqueImage(formencode.FancyValidator):
    """Use this class to determine the uniqueness of an Image"""
    def _to_python(self, value, state):
        image_q = meta.Session.query(model.Image)
        client_dn = request.environ['REPOSITORY_USER']
        uuid = h.image_uuid(client_dn, value)
        if image_q.filter(model.Image.uuid==uuid).first():
            state = 'CONFLICT'
            raise formencode.Invalid('conflict', value, state)
        else:
            return value


class NewImageForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    name = formencode.All(formencode.validators.String(not_empty=True),
                          UniqueImage())
    desc = formencode.validators.String(if_missing=None)

    os_variant = formencode.validators.String(if_missing=None)
    os_type = formencode.validators.String(if_missing=None)
    os_arch = formencode.validators.String(if_missing=None)
    hypervisor = formencode.validators.String(if_missing=None)

    owner_r = formencode.validators.Bool(if_missing=True)
    owner_w = formencode.validators.Bool(if_missing=True)
    group_r = formencode.validators.Bool(if_missing=False)
    other_r = formencode.validators.Bool(if_missing=False)

