import logging
import simplejson as json
from time import time
from datetime import datetime
from os import path

from pylons import request, response, session, tmpl_context as c, url, app_globals
from pylons.controllers.util import abort, redirect

from repository.lib.base import BaseController
from repository.lib import helpers as h

from repository.model import meta
from repository.model.image import Image
from repository.model.group import Group
from repository.model.representation import image_long, image_short
from repository.model.form import validate_new_image

import shutil

log = logging.getLogger(__name__)

#TODO: fix file upload.  it appears that the entire file is uploaded before params are validated

class ImagesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""

    def index(self, format='json'):
        """GET /repository/images: All items in the collection"""
        # url('repository_images')
        image_q = meta.Session.query(Image)
        data = [i for i in image_q]
        if format == 'json':
            response.headers['content-type'] = 'text/javascript'
            return json.dumps(image_short(*data))

    def create(self):
        """POST /repository/images: Create a new item"""

        params = validate_new_image(request.params)
        if 'file' not in params:
            abort(400, '400 Bad Request')

        #params.pop('file')
        #return json.dumps(params)

        g_uuid = h.group_uuid(params['group'])
        group = meta.Session.query(Group).filter(Group.uuid==g_uuid).first()
        if not group:
            abort(400, '400 Bad Request - group not found')

        # TODO: setting these values is overly verbose.  make it simple
        new_image = Image()
        # User settable values
        new_image.name = params['name']
        new_image.os_variant = params['os_variant']
        new_image.os_type = params['os_type']
        new_image.os_arch = params['os_arch']
        new_image.hypervisor = params['hypervisor']
        new_image.owner_r = params['owner_r']
        new_image.owner_w = params['owner_w']
        new_image.group_r = params['group_r']
        new_image.group_r = params['group_w']
        new_image.group_w = params['other_r']
        new_image.group_r = params['other_r']
        new_image.desc = params['desc']

        # Non-user settable values
        uuid = h.image_uuid(request.environ['REPOSITORY_USER_UUID'], params['name'])
        current_time = datetime.utcfromtimestamp(time())
        file_name = uuid + '_' + new_image.name

        new_image.owner_id = request.environ['REPOSITORY_USER_ID']
        new_image.group_id = group.id
        new_image.uuid = uuid
        new_image.version = 1
        new_image.uploaded = current_time
        new_image.modified = current_time
        new_image.url = ''
        new_image.previous = ''
        new_image.path = file_name

        # Deal with file upload
        try:
            image_file = params['file']
            local_path = path.join(app_globals.image_storage, file_name)
            permanent_file = open(local_path, 'w')
            shutil.copyfileobj(image_file.file, permanent_file)
            image_file.file.close()
            permanent_file.close()
        except Exception, e:
            abort(500, '500 Internal Error - Error uploading file %s' %e)

        meta.Session.add(new_image)
        meta.Session.commit()

    def new(self, format='html'):
        """GET /repository/images/new: Form to create a new item"""
        abort(501, '501 Not Implemented')

    def update(self, id):
        """PUT /repository/images/id: Update an existing item"""
        abort(501, '501 Not Implemented')

    def delete(self, id):
        """DELETE /repository/images/id: Delete an existing item"""
        abort(501, '501 Not Implemented')

    def show(self, id, format='json'):
        """GET /repository/images/id: Show a specific item"""
        # url('repository_image', id=ID)
        image = meta.Session.query(Image).filter(Image.uuid==id).first()
        if image:
            image_repr = image_long(image)
            if format == 'json':
                response.headers['content-type'] = 'text/javascript'
                return json.dumps(image_repr)
            elif format == 'file':
                local_path = path.join(app_globals.image_storage, image.path)
                image_file = open(local_path, 'rb')
                try:
                    # TODO: set proper header so the stream plays nice
                    return h.stream_img(image_file)
                except:
                    abort(500, '500 Internal Error')
        else:
            abort(404, '404 Not Found')

    def edit(self, id, format='html'):
        """GET /repository/images/id/edit: Form to edit an existing item"""
        # url('repository_edit_image', id=ID)
        abort(501, '501 Not Implemented')

