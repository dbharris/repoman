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

    def whoami(self, format='json'):
        """GET /repository/whoami: All items in the collection"""
        user = request.environ['REPOSITORY_USER']
        if user:
            if format == 'json':
                response.headers['content-type'] = app_globals.json_content_type
                return json.dumps(user_long(user))
            else:
            abort(501, '501 Not Implimented')
        else:
            abort(404, '404 Not Found')

