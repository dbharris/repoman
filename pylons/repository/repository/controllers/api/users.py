import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from repository.lib.base import BaseController

# custom imports

from repository.model import meta
from repository.model.user import User
from repository.model.group import Group
from repository.model.form import validate_new_user
from repository.model.representation import user_long, user_short
from repository.lib import helpers as h
from repository.lib.authorization import authorize, AllOf, AnyOf, NoneOf, HasPermission

from pylons import app_globals

import formencode
###

log = logging.getLogger(__name__)

def auth_403(message):
    abort(403, "403 Forbidden : '%s'" % message)


class UsersController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""

    @authorize(AllOf(HasPermission('user_list_all')), auth_403)
    def index(self, format='json'):
        """GET /repository/users: All items in the collection"""
        # url('repository_users')
        user_q = meta.Session.query(User)
        users = [user for user in user_q]
        if format == 'json':
            response.headers['content-type'] = app_globals.json_content_type
            return h.render_json(user_short(*users))
        else:
            abort(501, '501 Not Implemented')

    @authorize(AllOf(HasPermission('user_create')), auth_403)
    def create(self):
        """POST /repository/users: Create a new item"""

        params = validate_new_user(request.params)

        new_user = User(cert_dn=params['cert_dn'],
                        user_name=params['user_name'],
                        email=params['email'])
        new_user.full_name = params['full_name']
        new_user.suspended = params['suspended']

        # Deal with user groups
        groups = params['groups']
        if not groups:
            groups = [app_globals.default_user_group]
        else:
            groups = groups.rstrip(',').split(',')
            # Check for default user group
            if 'users' not in groups:
                groups.append(app_globals.default_user_group)

        # Do group membership
        #TODO: change from group name to group uuid for membership?
        group_q = meta.Session.query(Group)
        groups = [group_q.filter(Group.name==g).first() for g in groups]
        if None in groups:
            # abort if any specified group does not exist
            abort(400, '400 Bad Request')
        else:
            [new_user.groups.append(g) for g in groups]

        # Update the database
        meta.Session.add(new_user)
        meta.Session.commit()
        return h.render_json(user_long(new_user))

    def new(self, format='html'):
        """GET /repository/users/new: Form to create a new item"""
        abort(501, '501 Not Implemented')

    @authorize(AllOf(HasPermission('user_modify')), auth_403)
    def update(self, id):
        """PUT /repository/users/id: Update an existing item"""

        user = meta.Session.query(User).filter(User.user_name==id).first()
        if user:
            # What
            pass
        else:
            abort(404, '404 Not Found')

    @authorize(AllOf(HasPermission('user_delete')), auth_403)
    def delete(self, id):
        """DELETE /repository/users/id: Delete an existing item"""
        if not request.environ.get('REPOSITORY_USER_ADMIN'):
            abort(403, "403 Forbidden")

        user = meta.Session.query(User).filter(User.user_name==id).first()
        if user:
            # do something better here
            user.deleted = True
        else:
            abort(404, '404 Not Found')

#    @authorize(AllOf(HasPermission('user_list_all')), auth_403)
    def show(self, id, format='json'):
        """GET /repository/users/id: Show a specific item"""
        user = meta.Session.query(User).filter(User.user_name==id).first()
        if user:
            user_repr = user_long(user)
            if format=='json':
                response.headers['content-type'] = app_globals.json_content_type
                return h.render_json(user_repr)
            else:
                abort(501, '501 Not Implemented')
        else:
            abort(404, '404 Not Found')

    def edit(self, id, format='html'):
        """GET /repository/users/id/edit: Form to edit an existing item"""
        abort(501, '501 Not Implemented')

