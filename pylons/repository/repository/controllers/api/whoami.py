import logging
import simplejson as json

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from repository.lib.base import BaseController, render
from repository.model.representation import user_long
from repository.model import meta
from repository.model.user import User

from pylons import app_globals

log = logging.getLogger(__name__)

class WhoamiController(BaseController):
    """REST Controller styled on the Atom Publishing Protocol"""

    def index(self, format='html'):
        """GET /repository/whoami: All items in the collection"""
        user = request.environ['REPOSITORY_USER']
        if user:
            response.headers['content-type'] = app_globals.json_content_type
            return json.dumps(user_long(user))
        else:
            abort(404, '404 Not Found')

    def create(self):
        """POST /repository/whoami: Create a new item"""
        abort(400, '400 Bad Request')

    def new(self, format='html'):
        """GET /repository/whoami/new: Form to create a new item"""
        abort(400, '400 Bad Request')

    def update(self, id):
        """PUT /repository/whoami/id: Update an existing item"""
        abort(400, '400 Bad Request')

    def delete(self, id):
        """DELETE /repository/whoami/id: Delete an existing item"""
        abort(400, '400 Bad Request')

    def show(self, id, format='html'):
        """GET /repository/whoami/id: Show a specific item"""
        abort(400, '400 Bad Request')

    def edit(self, id, format='html'):
        """GET /repository/whoami/id/edit: Form to edit an existing item"""
        abort(400, '400 Bad Request')

