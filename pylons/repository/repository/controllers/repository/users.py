import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from repository.lib.base import BaseController
from repository.lib import helpers as h

#
import simplejson as json
from repository import model
from repository.model import meta
from repository.model.user import User
from repository.model.group import Group

log = logging.getLogger(__name__)

class UsersController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('user', 'users', controller='repository/users',
    #         path_prefix='/repository', name_prefix='repository_')

    def index(self, format='json'):
        """GET /repository/users: All items in the collection"""
        # url('repository_users')
        user_q = meta.Session.query(User)
        data = [{'id':u.id,
                 'name':u.name,
                 'email':u.email,
                 'client_dn':u.client_dn,
                 'admin':u.global_admin}
                 for u in user_q]
        if format == 'json':
            response.headers['content-type'] = 'text/javascript'
            return json.dumps(data)

    def create(self):
        """POST /repository/users: Create a new item"""
        # url('repository_users')

        # Expected Values
        client_dn = request.params.get('client_dn')
        name = request.params.get('name')
        email = request.params.get('email')
        admin = request.params.get('admin')
        suspended = request.params.get('suspended')
        groups = request.params.get('groups')

        user_q = meta.Session.query(User)
        user = user_q.filter(User.client_dn==client_dn).first()
        if user:
            headers = [('location', url('repository_users', id=user.id))]
            abort(409, '409 Conflict', headers=headers)
        elif admin and admin not in h.bool_values:
            abort(400, '400 Bad Request')
        elif suspended and suspended not in h.bool_values:
            abort(400, '400 Bad Request')
        elif client_dn and email and name:
            new_user = User(client_dn=client_dn, name=name, email=email)

            # Convert admin and suspended to True/False
            if admin:
                new_user.global_admin = h.bool_values[admin]
            if suspended:
                new_user.suspended = h.bool_values[suspended]

            # Deal with user groups
            if not groups:
                # No groups specified, add default group in
                groups = ['users']
            else:
                groups = groups.rstrip(',').split(',')
                # Check for default user group
                if 'users' not in groups:
                    groups.append('users')

            # Do group membership
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
        else:
            abort(400, '400 Bad Request')

    def new(self, format='html'):
        """GET /repository/users/new: Form to create a new item"""
        # url('repository_new_user')
        abort(501, '501 Not Implemented')

    def update(self, id):
        """PUT /repository/users/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('repository_user', id=ID),
        #           method='put')
        # url('repository_user', id=ID)
        abort(501, '501 Not Implemented')

    def delete(self, id):
        """DELETE /repository/users/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('repository_user', id=ID),
        #           method='delete')
        # url('repository_user', id=ID)
        abort(501, '501 Not Implemented')

    def show(self, id, format='json'):
        """GET /repository/users/id: Show a specific item"""
        # url('repository_user', id=ID)
        # Grab the user.
        user = meta.Session.query(User).filter(User.id==id).first()
        if user:
            data = {'id':user.id,
                    'name':user.name,
                    'email':user.email,
                    'client_dn':user.client_dn,
                    'admin':user.global_admin,
                    'suspended':user.suspended,
                    'images':[{'id':i.id,
                               'name':i.name,
                               'group_id':i.group_id}
                               for i in user.images],
                     'groups':[{'id':g.id,
                                'name':g.name}
                                for g in user.groups]}
            if format=='json':
                response.headers['content-type'] = 'text/javascript'
                return json.dumps(data)
        else:
            abort(404, '404 Not Found')
            return json.dumps(None)


    def edit(self, id, format='html'):
        """GET /repository/users/id/edit: Form to edit an existing item"""
        # url('repository_edit_user', id=ID)
        abort(501, '501 Not Implemented')
