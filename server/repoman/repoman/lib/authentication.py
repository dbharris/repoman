
# Project imports
from repoman.model import meta
from repoman.model.certificate import Certificate

# Standard imports
from time import strptime, gmtime

# Other imports


class UserAuthentication(object):
    """WSGI middleware authentication module

    This module is dependant on the mod_ssl environment variables.
    once the client has been authenticated by mod_ssl, this module will lookup
    the users Distinguished Name in the repoman database.
    If the user is not found in the database, a 403 Error will be returned.
    If the user is found in the database, the environment variables will be
    updated with:
        REPOMAN_USER_ID
        #others if needed
    """
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
        cert_q = meta.Session.query(Certificate)
        cert = cert_q.filter(Certificate.client_dn==client_dn).first()
        if not cert:
            start_response('403 Forbidden', [('Content-type', 'text/html')])
            return client_dn
            return ['Unknown user']
        elif cert.user.suspended:
            start_response('403 Forbidden', [('Content-type', 'text/html')])
            return ['Accout suspended.  Contact your administrator']
        elif not cert.user.suspended:
            # Update environ with user info
            new_env = environ.copy()
            new_env.update({"REPOMAN_USER":cert.user})
            return self.app(new_env, start_response)

