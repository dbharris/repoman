import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import validate
from pylons import app_globals

from repository.lib.base import BaseController
from repository.lib import helpers as h
from repository.model import meta
from repository.model.user import User
from repository.model.group import Group
from repository.model.form import validate_new_user
from repository.model.representation import user_long, user_short

#
import formencode
import simplejson as json

log = logging.getLogger(__name__)

class UsersController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""

    def index(self, format='json'):
        """GET /repository/users: All items in the collection"""
        # url('repository_users')
        user_q = meta.Session.query(User)
        users = [user for user in user_q]
        if format == 'json':
            response.headers['content-type'] = 'text/javascript'
            return json.dumps(user_short(*users))

    def create(self):
        """POST /repository/users: Create a new item"""
        if not request.environ.get('REPOSITORY_USER_ADMIN'):
            abort(403, "403 Forbidden")

        params = validate_new_user(request.params)

        new_user = User(client_dn=params['client_dn'],
                        name=params['name'],
                        email=params['email'])
        new_uuid = h.user_uuid(params['client_dn'])
        new_user.uuid = new_uuid

        # Deal with user groups
        if not params.get('groups'):
            groups = ['users']
        else:
            groups = groups.rstrip(',').split(',')
            # Check for default user group
            if 'users' not in groups:
                groups.append('users')

        # Do group membership
        #TODO: change from group name to group uuid for membership?
        group_q = meta.Session.query(Group)
        groups = [group_q.filter(Group.name==g).first() for g in groups]
        if None in groups:
            # abort if any specified group does not exist
            abort(400, '400 Bad Request - groups')
        else:
            [new_user.groups.append(g) for g in groups]

        # Update the database
        meta.Session.add(new_user)
        meta.Session.commit()

    def new(self, format='html'):
        """GET /repository/users/new: Form to create a new item"""
        abort(501, '501 Not Implemented')

    def update(self, id):
        """PUT /repository/users/id: Update an existing item"""
        abort(501, '501 Not Implemented')

    def delete(self, id):
        """DELETE /repository/users/id: Delete an existing item"""
        abort(501, '501 Not Implemented')

    def show(self, id, format='json'):
        """GET /repository/users/id: Show a specific item"""
        user = meta.Session.query(User).filter(User.uuid==id).first()
        if user:
            user_repr = user_long(user)
            if format=='json':
                response.headers['content-type'] = 'text/javascript'
                return json.dumps(user_repr)
        else:
            abort(404, '404 Not Found')

    def edit(self, id, format='html'):
        """GET /repository/users/id/edit: Form to edit an existing item"""
        abort(501, '501 Not Implemented')
