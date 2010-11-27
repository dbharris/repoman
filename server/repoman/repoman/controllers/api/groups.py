import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from repoman.lib.base import BaseController

# custom imports
from repoman.model import meta
from repoman.model.group import Group
from repoman.model.user import User
from repoman.model.permission import Permission
from repoman.model.form import validate_new_group
from repoman.lib import beautify
from repoman.lib import helpers as h
from repoman.lib.authorization import AllOf, AnyOf, NoneOf
from repoman.lib.authorization import authorize, inline_auth
from repoman.lib.authorization import HasPermission, IsAthuenticated, IsUser

from pylons import app_globals
###

log = logging.getLogger(__name__)


def auth_403(message):
    abort(403, "403 Forbidden : '%s'" % message)

class GroupsController(BaseController):

    def __before__(self):
        inline_auth(IsAthuenticated(), auth_403)

    def list_all(self, format='json'):
        group_q = meta.Session.query(Group)
        groups = [g for g in group_q]
        urls = [url('group', group=g.name, qualified=True) for g in groups]
        if format == 'json':
            response.headers['content-type'] = app_globals.json_content_type
            return h.render_json(urls)
        else:
            abort(501, '501 Not Implemented')

    def list_users(self, group, format='json'):
        pass

    def list_permissions(self, group, format='json'):
        pass

    @authorize(HasPermission('group_create'), auth_403)
    def new_group(self, format='json'):
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
        return h.render_json(beautify.group(new_group))

    @authorize(HasPermission('group_delete'), auth_403)
    def delete(self, group, format='json'):
        group = meta.Session.query(Group).filter(Group.name==group).first()
        if group:
            if not group.protected:
                meta.Session.delete(group)
                meta.Session.commit()
            else:
                abort(403, '403 Forbidden')
        else:
            abort(404, '404 Not Found')

    def show(self, group, format='json'):
        group = meta.Session.query(Group).filter(Group.name==group).first()
        if group:
            if format == 'json':
                response.headers['content-type'] = app_globals.json_content_type
                return h.render_json(beautify.group(group))
            else:
                abort(501, '501 Not Implemented')
        else:
            abort(404, '404 Not Found')

    @authorize(HasPermission('group_modify_membership'), auth_403)
    def add_user(self, group, user, format='json'):
        group = meta.Session.query(Group).filter(Group.name==group).first()
        user = meta.Session.query(User).filter(User.user_name==user).first()
        if group and user:
            if user not in group.users:
                group.users.append(user)
                meta.Session.commit()
        else:
            abort(404, '404 Not Found')

    @authorize(HasPermission('group_modify_membership'), auth_403)
    def remove_user(self, group, user, format='json'):
        group = meta.Session.query(Group).filter(Group.name==group).first()
        user = meta.Session.query(User).filter(User.user_name==user).first()
        if group and user:
            if user in group.users:
                group.users.remove(user)
                meta.Session.commit()
        else:
            abort(404, '404 Not Found')

    @authorize(HasPermission('group_modify_permissions'), auth_403)
    def add_permission(self, group, permission, format='json'):
        group = meta.Session.query(Group).filter(Group.name==group).first()
        perm = meta.Session.query(Permission)\
                           .filter(Permission.permission_name==permission)\
                           .first()
        if group and perm:
            if perm not in group.permissions:
                group.permissions.append(perm)
                meta.Session.commit()
        else:
            abort(404, '404 Not Found')

    @authorize(HasPermission('group_modify_permissions'), auth_403)
    def remove_permission(self, group, permission, format='json'):
        group = meta.Session.query(Group).filter(Group.name==group).first()
        perm = meta.Session.query(Permission)\
                           .filter(Permission.permission_name==permission)\
                           .first()
        if group and perm:
            if perm in group.permissions:
                group.permissions.remove(perm)
                meta.Session.commit()
        else:
            abort(404, '404 Not Found')

