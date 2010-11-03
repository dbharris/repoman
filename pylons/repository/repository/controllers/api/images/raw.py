import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from repository.lib.base import BaseController, render

# custom imports
from repository.model import meta
from repository.model.image import Image

###

log = logging.getLogger(__name__)

class RawController(BaseController):
    """Custom REST Controller for uploading and downloading raw images"""

    def post_upload(self, id):
        """POST /api/images/raw/id: upload the raw file to the id"""
        return self.upload(id)

    def put_upload(self, id):
        """PUT /api/images/raw/id: upload the raw file to the id"""
        return self.upload(id)

    def show(self, id, format=None):
        """GET /api/images/raw/id: return the raw file"""
        
    def upload(self, id):
        image_q = meta.Session.query(Image)
        image = image_q.filter(Image.uuid==id).first()
        return id
        if image:
            try:
                temp_file = params['file']
                return repr(type(temp_file))
                file_name = image.uuid + '_' + image.name
                local_path = path.join(app_globals.image_storage, image.file_name)
                # Move temp_file to local_path and close
                
                permanent_file = open(local_path, 'w')
                shutil.copyfileobj(image_file.file, permanent_file)
                image_file.file.close()
                permanent_file.close()
            except Exception, e:
                abort(500, '500 Internal Error - Error uploading file %s' %e)
        else:
            abort(404, '404 Item not found')
            
