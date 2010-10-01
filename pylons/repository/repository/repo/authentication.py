
# Project imports
from repository.model import meta
from repository.model.user import User
from repository.repo.helpers import environ_print

# Standard imports
from time import strptime, gmtime

# Other imports


class UserAuthentication(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        client_v_start = environ.get("SSL_CLIENT_V_START")
        client_v_end = environ.get("SSL_CLIENT_V_END")
        client_verify = environ.get("SSL_CLIENT_VERIFY")

        # check for certificate validity
        if client_verify not in ['SUCCESS']:
            start_response('403 Forbidden', [('Content-type', 'text/html')])
            return ['Client certificate not verified']

        # Check validity of certificate time
        try:
            start_time = strptime(client_v_start, "%b %d %H:%M:%S %Y %Z")
            end_time = strptime(client_v_end, "%b %d %H:%M:%S %Y %Z")
            now = gmtime()
            if not (start_time < now < end_time):
                start_response('403 Forbidden', [('Content-type', 'text/html')])
                return ['Certificate Expired']
        except:
            start_response('500 Internal Server Error', [('Content-type', 'text/html')])
            return ['The server has experienced an internal error.']

        #HACK: will a clients DN always have a CN?
        client_dn = environ.get("SSL_CLIENT_S_DN")
        if client_dn.count('/CN=') > 1:
            # Proxy cert.  need to remove the extra CNs' to get match in db
            while client_dn.count('/CN=') > 1:
                client_dn = client_dn[:client_dn.rindex('/CN=')]

        # Check if client is in the DB
        user_q = meta.Session.query(User)
        user = user_q.filter(User.client_dn==client_dn).first()
        if not user:
            start_response('403 Forbidden', [('Content-type', 'text/html')])
            return ['Unknown user']
        elif user.suspended:
            start_response('403 Forbidden', [('Content-type', 'text/html')])
            return ['Accout suspended.  Contact your administrator']
        elif not user.suspended:
            # Update environ with user info
            environ.update({"REPOSITORY_USER_ID":user.id})
            return self.app(environ, start_response)
