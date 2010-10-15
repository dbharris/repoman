import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from repository.lib.base import BaseController

#
import simplejson as json
from repository.model import meta
from repository.model.group import Group
from repository.model.user import User

log = logging.getLogger(__name__)

class GroupsController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('group', 'groups', controller='repository/groups',
    #         path_prefix='/repository', name_prefix='repository_')

    def index(self, format='json'):
        """GET /repository/groups: All items in the collection"""
        # url('repository_groups')
        group_q = meta.Session.query(Group)
        data = [{'id':g.id,
                 'name':g.name}
                 for g in group_q]
        if format == 'json':
            response.headers['content-type'] = 'text/javascript'
            return json.dumps(data)

    def create(self):
        """POST /repository/groups: Create a new item"""
        # url('repository_groups')
        group_q = meta.Session.query(Group)
        group = group_q.filter(Group.name==request.params['name']).first()
        if group:
            headers = [('location', url('repository_groups', id=group.id))]
            abort(409, '409 Conflict', headers=headers)
        elif not request.params.get('name'):
            abort(400, '400 Bad Request ~')
        else:
            name = request.params.get('name')
            users = request.params.get('users')
            new_group = Group(name=name)

            if users:
                user_ids = [(int(u)) for u in users.split(',')]
                user_q = meta.Session.query(User)
                users = [user_q.filter(User.id==u).first() for u in user_ids]
                if None in users:
                    # abort if any specified user does not exist
                    abort(400, '400 Bad Request')
                else:
                    [new_group.repo_users.append(u) for u in users]

            meta.Session.add(new_group)
            meta.Session.commit()

    def new(self, format='html'):
        """GET /repository/groups/new: Form to create a new item"""
        # url('repository_new_group')
        abort(501, '501 Not Implemented')

    def update(self, id):
        """PUT /repository/groups/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('repository_group', id=ID),
        #           method='put')
        # url('repository_group', id=ID)
        abort(501, '501 Not Implemented')

    def delete(self, id):
        """DELETE /repository/groups/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('repository_group', id=ID),
        #           method='delete')
        # url('repository_group', id=ID)
        abort(501, '501 Not Implemented')

    def show(self, id, format='json'):
        """GET /repository/groups/id: Show a specific item"""
        # url('repository_group', id=ID)
        group = meta.Session.query(Group).filter(Group.id==id).first()
        if group:
            data = {'id':group.id,
                    'name':group.name,
                    'users':[{'id':u.id,
                              'name':u.name,
                              'email':u.email,
                              'client_dn':u.client_dn}
                              for u in group.repo_users]}
            if format == 'json':
                response.headers['content-type'] = 'text/javascript'
                return json.dumps(data)
        else:
            return json.dumps(None)
            abort(404, '404 Not Found')

    def edit(self, id, format='html'):
        """GET /repository/groups/id/edit: Form to edit an existing item"""
        # url('repository_edit_group', id=ID)
        abort(501, '501 Not Implemented')
