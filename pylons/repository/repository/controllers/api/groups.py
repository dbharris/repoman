import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from repository.lib.base import BaseController

# custom imports
from repository.model import meta
from repository.model.group import Group
from repository.model.user import User
from repository.model.form import validate_new_group
from repository.model.representation import group_long, group_short
from repository.lib import helpers as h
from repository.lib.authorization import authorize, AllOf, AnyOf, NoneOf, HasPermission

from pylons import app_globals
###

log = logging.getLogger(__name__)


def auth_403(message):
    abort(403, "403 Forbidden : '%s'" % message)

class GroupsController(BaseController):

    def list_all(self, format='json'):
        pass

    def new_group(self, format='json'):
        pass

    def show(self, group, format='json'):
        pass

    def list_users(self, group, format='json'):
        pass

    def add_user(self, group, user, format='json'):
        pass

    def remove_user(self, group, user, format='json'):
        pass

    def list_permissions(self, group, format='json'):
        pass

    def add_permission(self, group, permission, format='json'):
        pass

    def remove_permission(self, group, permission, format='json'):
        pass



    @authorize(AllOf(HasPermission('group_list')), auth_403)
    def index(self, format='json'):
        """GET /repository/groups: All items in the collection"""
        # url('repository_groups')
        group_q = meta.Session.query(Group)
        data = [g for g in group_q]
        if format == 'json':
            response.headers['content-type'] = app_globals.json_content_type
            return h.render_json(group_short(*data))
        else:
            abort(501, '501 Not Implemented')

    @authorize(AllOf(HasPermission('group_create')), auth_403)
    def create(self):
        """POST /repository/groups: Create a new item"""

        if not request.environ.get('REPOSITORY_USER_ADMIN'):
            abort(403, "403 Forbidden")

        params = validate_new_group(request.params)

        new_group = Group(name=params['name'])

        users = params.get('users')
        if users:
            user_names = [u for u in users.split(',')]
            user_q = meta.Session.query(User)
            users = [user_q.filter(User.user_name==u).first() for u in user_names]
            if None in users:
                # abort if any specified user does not exist
                abort(400, '400 Bad Request - user does not exist')
            else:
                [new_group.repo_users.append(u) for u in users]

        meta.Session.add(new_group)
        meta.Session.commit()
        return h.render_json(group_long(new_group))

    def new(self, format='html'):
        """GET /repository/groups/new: Form to create a new item"""
        abort(501, '501 Not Implemented')

    @authorize(AllOf(HasPermission('group_modify')), auth_403)
    def update(self, id):
        """PUT /repository/groups/id: Update an existing item"""
        abort(501, '501 Not Implemented')

    @authorize(AllOf(HasPermission('group_delete')), auth_403)
    def delete(self, id):
        """DELETE /repository/groups/id: Delete an existing item"""
        abort(501, '501 Not Implemented')

    @authorize(AllOf(HasPermission('group_list')), auth_403)
    def show(self, id, format='json'):
        """GET /repository/groups/id: Show a specific item"""
        group = meta.Session.query(Group).filter(Group.name==id).first()
        if group:
            group_repr = group_long(group)
            if format == 'json':
                response.headers['content-type'] = app_globals.json_content_type
                return h.render_json(group_repr)
            else:
                abort(501, '501 Not Implemented')
        else:
            abort(404, '404 Not Found')

    def edit(self, id, format='html'):
        """GET /repository/groups/id/edit: Form to edit an existing item"""
        abort(501, '501 Not Implemented')

