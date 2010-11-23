import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from repoman.lib.base import BaseController

# custom imports

from repoman.model import meta
from repoman.model.user import User
from repoman.model.group import Group
from repoman.model.form import validate_new_user, validate_modify_user
from repoman.lib import helpers as h
from repoman.lib.authorization import AllOf, AnyOf, NoneOf
from repoman.lib.authorization import authorize, inline_auth
from repoman.lib.authorization import HasPermission, IsAthuenticated, IsUser
from repoman.lib import beautify
from repoman.lib import storage

from pylons import app_globals

import formencode
###

log = logging.getLogger(__name__)

def auth_403(message):
    abort(403, "403 Forbidden : '%s'" % message)


class UsersController(BaseController):

    def __before__(self):
        inline_auth(IsAthuenticated(), auth_403)

    def list_all(self, format='json'):
        user_q = meta.Session.query(User).filter(User.deleted!=True)
        users = [user.user_name for user in user_q]
        urls = [url('user', user=u, qualified=True) for u in users]
        if format == 'json':
            response.headers['content-type'] = app_globals.json_content_type
            return h.render_json(urls)
        else:
            abort(501, '501 Not Implemented')

    @authorize(AllOf(HasPermission('user_create')), auth_403)
    def new_user(self, format='json'):
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
        return h.render_json(beautify.user(new_user))

    #authorization is inside function
    def modify_user(self, user, format='json'):
        inline_auth(AnyOf(AllOf(HasPermission('user_modify_self'), IsUser(user)),
                          HasPermission('user_modify')),
                          auth_403)

        params = validate_modify_user(request.params)

        user_q = meta.Session.query(User)
        user = user_q.filter(User.user_name==user).first()

        if user:
            for k,v in params.iteritems():
                if v:
                    setattr(user, k, v)
            meta.Session.commit()
        else:
            abort(404, '404 Not Found')

    @authorize(HasPermission('user_delete'), auth_403)
    def delete_user(self, user, format='json'):
        user = meta.Session.query(User).filter(User.user_name==user).first()
        if user:
            for i in user.images:
                storage.delete_image(i)
                meta.Session.delete(i.checksum)
                meta.Session.delete(i.shared)
                meta.Session.delete(i)
            meta.Session.delete(user)
            meta.Session.commit()
        else:
            abort(404, '404 Not Found')

    def show(self, user, format='json'):
        user = meta.Session.query(User).filter(User.user_name==user).first()
        if user:
            if format=='json':
                response.headers['content-type'] = app_globals.json_content_type
                return h.render_json(beautify.user(user))
            else:
                abort(501, '501 Not Implemented')
        else:
            abort(404, '404 Not Found')

    def list_images(self, user, format='json'):
        user = meta.Session.query(User).filter(User.user_name==user).first()
        if user:
            images = user.images
            if format=='json':
                response.headers['content-type'] = app_globals.json_content_type
                return h.render_json([url('image_by_user', image=i.name, user=user.user_name, qualified=True) for i in images])
            else:
                abort(501, '501 Not Implemented')
        else:
            abort(404, '404 Not Found')

    def list_groups(self, user, format='json'):
        user = meta.Session.query(User).filter(User.user_name==user).first()
        if user:
            groups = user.groups
            if format=='json':
                response.headers['content-type'] = app_globals.json_content_type
                return h.render_json([url('group', group=g.name, qualified=True) for g in groups])
            else:
                abort(501, '501 Not Implemented')
        else:
            abort(404, '404 Not Found')

    def list_my_shared_images(self, user, format='json'):
        user = meta.Session.query(User).filter(User.user_name==user).first()
        if user:
            shared = []
            for i in user.images:
                if i.shared.users or i.shared.groups:
                    shared.append(i)
            if format=='json':
                response.headers['content-type'] = app_globals.json_content_type
                return h.render_json([url('image_by_user', user=user.user_name, image=i.name, qualified=True) for i in shared])
            else:
                abort(501, '501 Not Implemented')
        else:
            abort(404, '404 Not Found')

    def get_shared_with_me(self, user, format='json'):
        user = meta.Session.query(User).filter(User.user_name==user).first()
        if user:
            shared = user.shared_images
            for g in user.groups:
                shared.extend(g.shared_images)
            shared = list(set(shared))
            if format=='json':
                response.headers['content-type'] = app_globals.json_content_type
                return h.render_json([url('image_by_user', image=s.image.name, user=s.image.owner.user_name, qualified=True) for s in shared])
            else:
                abort(501, '501 Not Implemented')
        else:
            abort(404, '404 Not Found')

