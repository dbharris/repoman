import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from repoman.lib.base import BaseController, render

# custom imports
from sqlalchemy import join

from repoman.model import meta
from repoman.model.image import Image
from repoman.model.group import Group
from repoman.model.user import User
from repoman.model.form import validate_new_image, validate_modify_image
from repoman.lib.authorization import AllOf, AnyOf, NoneOf
from repoman.lib.authorization import authorize, inline_auth
from repoman.lib.authorization import HasPermission, IsAthuenticated, IsUser, OwnsImage, SharedWith, MemberOf
from repoman.lib import beautify, storage
from repoman.lib import helpers as h
from pylons import app_globals

from time import time
from datetime import datetime
from os import path, remove, rename
import shutil
###

log = logging.getLogger(__name__)

def auth_403(message):
    abort(403, "403 Forbidden : '%s'" % message)

class ImagesController(BaseController):
    #TODO: move image streaming and upload functions to a new module
    #TODO: set mime-type for streaming file
    #TODO: calc md5sum for image
    #TODO: set image size after upload

    def __before__(self):
        inline_auth(IsAthuenticated(), auth_403)

    def user_share_by_user(self, user, image, share_with, format='json'):
        image = meta.Session.query(Image)\
                            .filter(Image.name==image)\
                            .filter(Image.owner.has(User.user_name==user))\
                            .first()

        if image:
            inline_auth(OwnsImage(image), auth_403)
            user = meta.Session.query(User)\
                               .filter(User.user_name==share_with)\
                               .first()
            if not user:
                abort(400, '400 Bad Request')
            if user in image.shared.users:
                return
            else:
                image.shared.users.append(user)
                meta.Session.commit()
        else:
            abort(404, '404 Not Found')

    def group_share_by_user(self, user, image, share_with, format='json'):
        image = meta.Session.query(Image)\
                            .filter(Image.name==image)\
                            .filter(Image.owner.has(User.user_name==user))\
                            .first()

        if image:
            inline_auth(AllOf(OwnsImage(image), MemberOf(share_with)), auth_403)
            group = meta.Session.query(Group)\
                                .filter(Group.name==share_with).first()
            if not group:
                abort(400, '400 Bad Request')
            if group in image.shared.groups:
                return
            else:
                image.shared.groups.append(group)
                meta.Session.commit()
        else:
            abort(404, '404 Not Found')

    def user_unshare_by_user(self, user, image, share_with, format='json'):
        image = meta.Session.query(Image)\
                            .filter(Image.name==image)\
                            .filter(Image.owner.has(User.user_name==user))\
                            .first()

        if image:
            inline_auth(OwnsImage(image), auth_403)
            user = meta.Session.query(User)\
                               .filter(User.user_name==share_with).first()
            if not user:
                abort(400, '400 Bad Request')
            if user in image.shared.users:
                image.shared.users.remove(user)
                meta.Session.commit()
        else:
            abort(404, '404 Not Found')

    def group_unshare_by_user(self, user, image, share_with, format='json'):
        image = meta.Session.query(Image)\
                            .filter(Image.name==image)\
                            .filter(Image.owner.has(User.user_name==user))\
                            .first()

        if image:
            inline_auth(OwnsImage(image), auth_403)
            group = meta.Session.query(Group)\
                                .filter(Group.name==share_with).first()
            if not group:
                abort(400, '400 Bad Request')
            if group in image.shared.groups:
                image.shared.groups.remove(group)
                meta.Session.commit()
        else:
            abort(404, '404 Not Found')


    def user_share(self, image, share_with, format='json'):
        user = request.environ['REPOMAN_USER'].user_name
        return self.user_share_by_user(user=user,
                                        image=image,
                                        share_with=share_with,
                                        format=format)

    def group_share(self, image, share_with, format='json'):
        user = request.environ['REPOMAN_USER'].user_name
        return self.group_share_by_user(user=user,
                                         image=image,
                                         share_with=share_with,
                                         format=format)

    def user_unshare(self, image, share_with, format='json'):
        user = request.environ['REPOMAN_USER'].user_name
        return self.user_unshare_by_user(user=user,
                                          image=image,
                                          share_with=share_with,
                                          format=format)

    def group_unshare(self, image, share_with, format='json'):
        user = request.environ['REPOMAN_USER'].user_name
        return self.group_unshare_by_user(user=user,
                                           image=image,
                                           share_with=share_with,
                                           format=format)

    def upload_raw_by_user(self, user, image, format='json'):
        image_q = meta.Session.query(Image)
        image = image_q.filter(Image.name==image)\
                       .filter(Image.owner.has(User.user_name==user)).first()

        if image:
            inline_auth(OwnsImage(image), auth_403)
            try:
                temp_file = request.params['file']
                file_name = user + '_' + image.name
                temp_storage = file_name + '.tmp'
                final_path = path.join(app_globals.image_storage, file_name)
                temp_path = path.join(app_globals.image_storage, temp_storage)
                permanent_file = open(temp_path, 'w')
                shutil.copyfileobj(temp_file.file, permanent_file)
                permanent_file.close()
                temp_file.file.close()
                rename(temp_path, final_path)
            except Exception, e:
                remove(temp_path)
                remove(final_path)
                abort(500, '500 Internal Error - Error uploading file %s' %e)

            image.raw_uploaded = True
            image.path = file_name
            image.version += 1
            image.modified = datetime.utcfromtimestamp(time())
            meta.Session.commit()
        else:
            abort(404, '404 Item not found')

    def upload_raw(self, image, format='json'):
        user = request.environ['REPOMAN_USER'].user_name
        return self.upload_raw_by_user(user=user, image=image, format=format)

    def show_meta_by_user(self, user, image, format='json'):
        image_q = meta.Session.query(Image)
        image = image_q.filter(Image.name==image)\
                       .filter(Image.owner.has(User.user_name==user))\
                       .first()

        if image:
            inline_auth(AnyOf(OwnsImage(image), SharedWith(image)), auth_403)
            if format == 'json':
                response.headers['content-type'] = app_globals.json_content_type
                return h.render_json(beautify.image(image))
            else:
                abort(501, '501 Not Implemented')
        else:
            abort(404, '404 Not Found')

    def modify_meta_by_user(self, user, image, format='json'):
        params = validate_modify_image(request.params)

        image_q = meta.Session.query(Image)
        image = image_q.filter(Image.name==image)\
                       .filter(Image.owner.has(User.user_name==user))\
                       .first()

        if image:
            inline_auth(AnyOf(OwnsImage(image), HasPermission('image_modify')), auth_403)
            for k,v in params.iteritems():
                if v:
                    setattr(image, k, v)
            image.modified = datetime.utcfromtimestamp(time())
            meta.Session.commit()
        else:
            abort(404, '404 Not Found')

    def delete_by_user(self, user, image, format='json'):
        image_q = meta.Session.query(Image)
        image = image_q.filter(Image.name==image)\
                       .filter(Image.owner.has(User.user_name==user))\
                       .first()

        if image:
            inline_auth(AnyOf(OwnsImage(image), HasPermission('image_delete')), auth_403)
            try:
                storage.delete_image(image)
            except Exception, e:
                abort(500, 'Unable to remove image file from storage')
            meta.Session.delete(image.checksum)
            meta.Session.delete(image.shared)
            meta.Session.delete(image)
            meta.Session.commit()
        else:
            abort(404, '404 Not Found')

    def show_meta(self, image, format='json'):
        user = request.environ['REPOMAN_USER'].user_name
        return self.show_meta_by_user(user=user, image=image, format=format)

    def modify_meta(self, image, format='json'):
        user = request.environ['REPOMAN_USER'].user_name
        return self.modify_meta_by_user(user=user, image=image, format=format)

    def delete(self, image, format='json'):
        user = request.environ['REPOMAN_USER'].user_name
        return self.delete_by_user(user=user, image=image, format=format)

    def list_all(self, format='json'):
        images = meta.Session.query(Image).all()
        urls = [url('image_by_user', user=i.owner.user_name,
                image=i.name, qualified=True) for i in images]
        if format == 'json':
            response.headers['content-type'] = app_globals.json_content_type
            return h.render_json(urls)
        else:
            abort(501, '501 Not Implemented')

    @authorize(HasPermission('image_create'), auth_403)
    def new(self, format='json'):
        params = validate_new_image(request.params)

        if params['user_name']:
            user_q = meta.Session.query(User)
            user = user_q.filter(User.user_name==params['user_name']).first()
        else:
            user = request.environ['REPOMAN_USER']

        if not user:
                abort(400, '400 Bad Request')

        # check for conflict
        image_q = meta.Session.query(Image).filter(Image.name==params['name'])
        image = image_q.filter(Image.owner.has(User.user_name==user.user_name)).first()
        if image:
            abort(409, '409 Conflict')

        # TODO: setting these values is overly verbose.  make it simple
        new_image = Image()
        # User settable values
        new_image.name = params['name']
        new_image.os_variant = params['os_variant']
        new_image.os_type = params['os_type']
        new_image.os_arch = params['os_arch']
        new_image.hypervisor = params['hypervisor']
        new_image.description = params['description']
        new_image.expires = params['expires']
        new_image.read_only = params['read_only']
        new_image.unauthenticated_access = params['unauthenticated_access']

        # Non-user settable values
        uuid = h.image_uuid()
        current_time = datetime.utcfromtimestamp(time())
        file_name = uuid + '_' + new_image.name

        new_image.owner = user
        new_image.uuid = uuid
        new_image.uploaded = current_time
        new_image.modified = current_time
        new_image.path = file_name
        new_image.raw_uploaded = False

        meta.Session.add(new_image)
        meta.Session.commit()

        response.headers['Location'] = url('raw_by_user',
                                           user=user.user_name,
                                           image=new_image.name)
        response.status = ("201 Object created.  upload raw file to 'Location'")
        return h.render_json(beautify.image(new_image))

