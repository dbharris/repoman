import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from repository.lib.base import BaseController

#
import simplejson as json
from repository.model import meta
from repository.model.image import Image

log = logging.getLogger(__name__)

class ImagesController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""
    # To properly map this controller, ensure your config/routing.py
    # file has a resource setup:
    #     map.resource('image', 'images', controller='repository/images',
    #         path_prefix='/repository', name_prefix='repository_')

    def index(self, format='json'):
        """GET /repository/images: All items in the collection"""
        # url('repository_images')
        image_q = meta.Session.query(Image)
        data = [{'id':i.id,
                 'name':i.name,
                 'owner_id':i.owner_id,
                 'group_id':group_id}
                 for i in image_q]
        if format == 'json':
            response.headers['content-type'] = 'text/javascript'
            return json.dumps(data)

    def create(self):
        """POST /repository/images: Create a new item"""
        # url('repository_images')
        abort(501, '501 Not Implemented')

    def new(self, format='html'):
        """GET /repository/images/new: Form to create a new item"""
        # url('repository_new_image')
        abort(501, '501 Not Implemented')

    def update(self, id):
        """PUT /repository/images/id: Update an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="PUT" />
        # Or using helpers:
        #    h.form(url('repository_image', id=ID),
        #           method='put')
        # url('repository_image', id=ID)
        abort(501, '501 Not Implemented')

    def delete(self, id):
        """DELETE /repository/images/id: Delete an existing item"""
        # Forms posted to this method should contain a hidden field:
        #    <input type="hidden" name="_method" value="DELETE" />
        # Or using helpers:
        #    h.form(url('repository_image', id=ID),
        #           method='delete')
        # url('repository_image', id=ID)
        abort(501, '501 Not Implemented')

    def show(self, id, format='json'):
        """GET /repository/images/id: Show a specific item"""
        # url('repository_image', id=ID)
        image = meta.Session.query(Image).filter(Image.id==id).first()
        if image:
            data = {'id':image.id,
                    'name':image.name,
                    'owner_id':image.owner_id,
                    'group_id':image.group_id,
                    'permissions':{'owner_r':image.owner_r,
                                   'owner_w':image.owner_w,
                                   'group_r':image.group_r,
                                   'group_w':image.group_w,
                                   'other_r':image.other_r,
                                   'other_w':image.other_w},
                     'desc':image.desc}
            if format == 'json':
                response.headers['content-type'] = 'text/javascript'
                return json.dumps(data)
        else:
            abort(404, '404 Not Found')

    def edit(self, id, format='html'):
        """GET /repository/images/id/edit: Form to edit an existing item"""
        # url('repository_edit_image', id=ID)
        abort(501, '501 Not Implemented')
