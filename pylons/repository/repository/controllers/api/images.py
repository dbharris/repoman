import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from repository.lib.base import BaseController, render

# custom imports
from sqlalchemy import join

from repository.model import meta
from repository.model.image import Image
from repository.model.group import Group
from repository.model.user import User
from repository.model.form import validate_new_image, validate_image_share
from repository.lib import beautify
from repository.lib import helpers as h
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

    def share_by_user(self, user, image, format='json'):
        params = validate_image_share(request.params)

        image_q = meta.Session.query(Image)
        image = image_q.filter(Image.name==image)\
                       .filter(Image.owner.has(User.user_name==user)).first()

        if image:
            if params['user_name']:
                user = meta.Session.query(User)\
                                   .filter(User.user_name==params['user_name'])\
                                   .first()
                if not user:
                    abort(400, '400 Bad Request')
                if user not in image.shared.users:
                    image.shared.users.append(user)
                    meta.Session.commit()
            elif params['group']:
                group = meta.Session.query(Image)\
                                   .filter(Image.user_name==params['group'])\
                                   .first()
                if not group:
                    abort(400, '400 Bad Request')
                if group not in image.shared.groups:
                    image.shared.groups.append(group)
                    meta.Session.commit()
        else:
            abort(404, '404 Not Found')


    def unshare_by_user(self, user, image, format='json'):

        params = validate_image_share(request.params)

        image_q = meta.Session.query(Image)\
                       .filter(Image.owner.has(User.user_name==user)).first()

        if image:
            if params['user_name']:
                user = meta.Session.query(User)\
                                   .filter(User.user_name==params['user_name'])\
                                   .first()
                return 'a'
                if user:
                    if user in image.shared.users:
                        image.shared.users.remove(user)
                        meta.Session.commit()
                else:
                    abort(400, '400 Bad Request')
            elif params['group']:
                group = meta.Session.query(Image)\
                                   .filter(Image.user_name==params['group'])\
                                   .first()
                if not group:
                    abort(400, '400 Bad Request')
                if group in image.shared.groups:
                    image.shared.groups.remove(group)
                    meta.Session.commit()
        else:
            abort(404, '404 Not Found')

    def share(self, image, format='json'):
        user = request.environ['REPOSITORY_USER'].user_name
        self.share_by_user(user=user, image=image, format=format)

    def unshare(self, image, format='json'):
        user = request.environ['REPOSITORY_USER'].user_name
        self.unshare_by_user(user=user, image=image, format=format)

    def get_raw_by_user(self, user, image, format='json'):
        image_q = meta.Session.query(Image)
        image = image_q.filter(Image.name==image)\
                       .filter(Image.owner.has(User.user_name==user))\
                       .first()

        if not image:
            abort(404, '404 Not Found')
        else:
            if not image.raw_uploaded:
                abort(404, '404 Not Found')

            file_path = path.join(app_globals.image_storage, image.path)
            image_file = open(file_path, 'rb')
            try:
                return h.stream_img(image_file)
            except:
                abort(500, '500 Internal Error')

    def upload_raw_by_user(self, user, image, format='json'):
        #if user != request.environ['REPOSITORY_USER'].user_name:
        #    abort(403, '403 forbidden')

        image_q = meta.Session.query(Image)
        image = image_q.filter(Image.name==image)\
                       .filter(Image.owner.has(User.user_name==user)).first()

        if image:
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

    def get_raw(self, image, format='json'):
        user = request.environ['REPOSITORY_USER'].user_name
        self.get_raw_by_user(user=user, image=image, format=format)

    def upload_raw(self, image, format='json'):
        user = request.environ['REPOSITORY_USER'].user_name
        self.upload_raw_by_user(user=user, image=image, format=format)

    def show_meta_by_user(self, user, image, format='json'):
        image_q = meta.Session.query(Image)
        image = image_q.filter(Image.name==image)\
                       .filter(Image.owner.has(User.user_name==user))\
                       .first()
        if image:
            if format == 'json':
                response.headers['content-type'] = app_globals.json_content_type
                return h.render_json(beautify.image(image))
            else:
                abort(501, '501 Not Implemented')
        else:
            abort(404, '404 Not Found')

    def modify_meta_by_user(self, user, image, format='json'):
        pass

    def delete_by_user(self, user, image, format='json'):
        pass

    def delete(self, image, format='json'):
        user = request.environ['REPOSITORY_USER'].user_name
        self.delete_by_user(user=user, image=image, format=format)

    def show_meta(self, image, format='json'):
        user = request.environ['REPOSITORY_USER'].user_name
        self.show_meta_by_user(user=user, image=image, format=format)

    def modify_meta(self, image, format='json'):
        user = request.environ['REPOSITORY_USER'].user_name
        self.modify_meta_by_user(user=user, image=image, format=format)

    def delete(self, image, format='json'):
        user = request.environ['REPOSITORY_USER'].user_name
        self.delete_by_user(user=user, image=image, format=format)

    def list_all(self, format='json'):
        images = meta.Session.query(Image).all()
        urls = [url('image_by_user', user=i.owner.user_name,
                image=i.name, qualified=True) for i in images]
        if format == 'json':
            response.headers['content-type'] = app_globals.json_content_type
            return h.render_json(urls)
        else:
            abort(501, '501 Not Implemented')

    def new(self, format='json'):
        params = validate_new_image(request.params)

        if params['user_name']:
            user_q = meta.Session.query(User)
            user = user_q.filter(User.user_name==params['user_name']).first()
        else:
            user = request.environ['REPOSITORY_USER']

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
        new_image.allow_http_get = params['allow_http_get']

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

        response.headers['Location'] = url('raw/%s' % uuid)
        response.status = ("201 Object created.  upload raw file to 'Location'")
        return h.render_json(beautify.image(new_image))

