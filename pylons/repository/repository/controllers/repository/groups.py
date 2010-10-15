import logging
import simplejson as json

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from repository.lib.base import BaseController
from repository.lib import helpers as h

from repository.model import meta
from repository.model.group import Group
from repository.model.user import User
from repository.model.form import validate_new_group
from repository.model.representation import group_long, group_short

log = logging.getLogger(__name__)

class GroupsController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""

    def index(self, format='json'):
        """GET /repository/groups: All items in the collection"""
        # url('repository_groups')
        group_q = meta.Session.query(Group)
        data = [g for g in group_q]
        if format == 'json':
            response.headers['content-type'] = 'text/javascript'
            return json.dumps(group_short(*data))

    def create(self):
        """POST /repository/groups: Create a new item"""

        if not request.environ.get('REPOSITORY_USER_ADMIN'):
            abort(403, "403 Forbidden")

        params = validate_new_group(request.params)

        new_group = Group(name=params['name'])
        new_group.uuid = h.group_uuid(params['name'])

        users = params.get('users')
        if users:
            user_uuids = [u for u in users.split(',')]
            user_q = meta.Session.query(User)
            users = [user_q.filter(User.uuid==u).first() for u in user_uuids]
            if None in users:
                # abort if any specified user does not exist
                abort(400, '400 Bad Request - user does not exist')
            else:
                [new_group.repo_users.append(u) for u in users]

        meta.Session.add(new_group)
        meta.Session.commit()

    def new(self, format='html'):
        """GET /repository/groups/new: Form to create a new item"""
        abort(501, '501 Not Implemented')

    def update(self, id):
        """PUT /repository/groups/id: Update an existing item"""
        abort(501, '501 Not Implemented')

    def delete(self, id):
        """DELETE /repository/groups/id: Delete an existing item"""
        abort(501, '501 Not Implemented')

    def show(self, id, format='json'):
        """GET /repository/groups/id: Show a specific item"""
        group = meta.Session.query(Group).filter(Group.uuid==id).first()
        if group:
            group_repr = group_long(group)
            if format == 'json':
                response.headers['content-type'] = 'text/javascript'
                return json.dumps(group_repr)
        else:
            abort(404, '404 Not Found')

    def edit(self, id, format='html'):
        """GET /repository/groups/id/edit: Form to edit an existing item"""
        abort(501, '501 Not Implemented')
