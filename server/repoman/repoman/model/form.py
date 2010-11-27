import formencode
import uuid

from pylons import app_globals, url, request
from pylons.controllers.util import abort, redirect

from repoman.lib import helpers as h
from repoman.model import meta
from repoman import model

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
            if v.state=='CONFLICT':
                abort(409, '409 Conflict')
            else:
                abort(400, '400 Bad Request - validate_new_user')
    else:
        return result

def validate_modify_user(params):
    schema = ModifyUserForm()
    try:
        result = schema.to_python(params)
    except formencode.validators.Invalid, error:
        for e,v in error.error_dict.iteritems():
            if v.state=='CONFLICT':
                abort(409, '409 Conflict')
            else:
                abort(400, '400 Bad Request - validate_modify_user')
    else:
        return result

class UniqueUsername(formencode.FancyValidator):
    """Use this class to define what makes a unique user."""
    def _to_python(self, value, state):
        user_q = meta.Session.query(model.User)
        if user_q.filter(model.User.user_name==value).first():
            state = 'CONFLICT'
            raise formencode.Invalid('conflict', value, state)
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

class UniqueEmail(formencode.FancyValidator):
    def _to_python(self, value, state):
        user_q = meta.Session.query(model.User)
        if user_q.filter(model.User.email==value).first():
            state = 'CONFLICT'
            raise formencode.Invalid('conflict', value, state)
        else:
            return value

class ModifyUserForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    # What fields should be editable by the user?
    full_name = formencode.validators.String(if_missing=None)

class NewUserForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    # Manditory fields here
    user_name = formencode.All(formencode.validators.String(not_empty=True),
                               UniqueUsername())
    cert_dn = formencode.All(formencode.validators.String(not_empty=True),
                             UniqueCertDN())
    email = formencode.All(formencode.validators.String(not_empty=True),
                           formencode.validators.Email(),
                           UniqueEmail())
    full_name = formencode.validators.String(not_empty=True)

    # Default fields here
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
                abort(400, '400 Bad Request')
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

def validate_modify_image(params):
    schema = ModifyImageForm()
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

class NewImageForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    user_name = formencode.validators.String(if_missing=None)

    name = formencode.validators.String(not_empty=True)
    description = formencode.validators.String(if_missing=None)

    os_variant = formencode.validators.String(if_missing=None)
    os_type = formencode.validators.String(if_missing=None)
    os_arch = formencode.validators.String(if_missing=None)
    hypervisor = formencode.validators.String(if_missing=None)

    expires = formencode.validators.String(if_missing=None)

    #expires = formencode.validators.DateTime???
    read_only = formencode.validators.Bool(if_missing=False)
    unauthenticated_access = formencode.validators.Bool(if_missing=False)

class ModifyImageForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    name = formencode.validators.String(if_missing=None)
    description = formencode.validators.String(if_missing=None)

    os_variant = formencode.validators.String(if_missing=None)
    os_type = formencode.validators.String(if_missing=None)
    os_arch = formencode.validators.String(if_missing=None)
    hypervisor = formencode.validators.String(if_missing=None)

    expires = formencode.validators.String(if_missing=None)

    #expires = formencode.validators.DateTime???
    read_only = formencode.validators.Bool(if_missing=None)
    unauthenticated_access = formencode.validators.Bool(if_missing=None)

def validate_raw_image(params):
    schema = NewImageForm()
    try:
        result = schema.to_python(params)
    except formencode.validators.Invalid, error:
        for e,v in error.error_dict.iteritems():
            if e=='name' and v.state=='CONFLICT':
                abort(409, '409 Conflict')
            else:
                abort(400, '400 Bad Request')
    else:
        return result

class RawImageForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    #TODO: Add file validator here

