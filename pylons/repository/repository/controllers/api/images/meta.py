import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from repository.lib.base import BaseController, render

# custom imports
from repository.model import meta
from repository.model.image import Image
from repository.model.group import Group
from repository.model.user import User
from repository.model.representation import image_long, image_short
from repository.model.form import validate_new_image
from repository.lib import helpers as h
from pylons import app_globals

from time import time
from datetime import datetime
from os import path
###

log = logging.getLogger(__name__)

class MetaController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""

    def index(self, format='json'):
        """GET /api/images/meta: All items in the collection"""
        image_q = meta.Session.query(Image)
        data = [i for i in image_q]
        if format == 'json':
            response.headers['content-type'] = app_globals.json_content_type
            return h.render_json(image_short(*data))
        else:
            abort(501, '501 Not Implemented')

    def create(self):
        """POST /api/images/meta: Create a new item"""
        params = validate_new_image(request.params)

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
        new_image.other_r = params['other_r']
        new_image.desc = params['desc']

        # Non-user settable values
        uuid = h.image_uuid(request.environ['REPOSITORY_USER_UUID'], params['name'])
        current_time = datetime.utcfromtimestamp(time())
        file_name = uuid + '_' + new_image.name

        new_image.owner = request.environ['REPOSITORY_USER']
        new_image.uuid = uuid
        new_image.version = 1
        new_image.uploaded = current_time
        new_image.modified = current_time
        new_image.url = ''
        new_image.previous = ''
        new_image.path = file_name

        meta.Session.add(new_image)
        meta.Session.commit()

        response.headers['Location'] = url('raw/%s' % uuid)
        response.status = ("201 Object created.  upload raw file to 'Location'")
        return h.render_json(image_long(new_image))

    def new(self, format='html'):
        """GET /api/images/meta/new: Form to create a new item"""
        abort(501, '501 Not Implemented')

    def update(self, id):
        """PUT /api/images/meta/id: Update an existing item"""
        abort(501, '501 Not Implemented')

    def delete(self, id):
        """DELETE /api/images/meta/id: Delete an existing item"""
        abort(501, '501 Not Implemented')

    def show(self, id, format='json'):
        """GET /api/images/meta/id: Show a specific item"""
        image = meta.Session.query(Image).filter(Image.uuid==id).first()
        if image:
            image_repr = image_long(image)
            if format == 'json':
                response.headers['content-type'] = app_globals.json_content_type
                return h.render_json(image_long(image_repr))
            else:
                abort(501, '501 Not Implemented')
        else:
            abort(404, '404 Not Found')

    def edit(self, id, format='html'):
        """GET /api/images/meta/id/edit: Form to edit an existing item"""
        abort(501, '501 Not Implemented')

