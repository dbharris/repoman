
# Project imports
from repoman.model import meta
from repoman.model.certificate import Certificate

# Standard imports
from time import strptime, gmtime

# Other imports

def demo_app(environ,start_response):
    from StringIO import StringIO
    stdout = StringIO()
    print >>stdout, "Hello world!"
    print >>stdout
    h = environ.items(); h.sort()
    for k,v in h:
        print >>stdout, k,'=', repr(v)
    start_response("200 OK", [('Content-Type','text/plain')])
    return [stdout.getvalue()]


class UserAuthentication(object):
    """WSGI middleware authentication module

    This module is dependant on the mod_ssl environment variables.
    once the client has been authenticated by mod_ssl, this module will lookup
    the users Distinguished Name in the repoman database.
    If the user is not found in the database, a 403 Error will be returned.
    If the user is found in the database, the environment variables will be
    updated with:
        REPOMAN_USER
        #others if needed
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        client_verify = environ.get("SSL_CLIENT_VERIFY")

        if client_verify not in ['SUCCESS']:
            # Enter repoman as an unauthenticated user
            new_env = environ.copy()
            new_env.update({"AUTHENTICATED":False})
            return self.app(new_env, start_response)

        else:
            client_v_start = environ.get("SSL_CLIENT_V_START")
            client_v_end = environ.get("SSL_CLIENT_V_END")

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
            if cert:
                if cert.user.suspended:
                    start_response('403 Forbidden', [('Content-type', 'text/html')])
                    return ['Accout suspended.  Contact your administrator']
                elif not cert.user.suspended:
                    # Update environ with user info
                    new_env = environ.copy()
                    new_env.update({"AUTHENTICATED":True})
                    new_env.update({"REPOMAN_USER":cert.user})
                    return self.app(new_env, start_response)
            else:
                new_env = environ.copy()
                new_env.update({"AUTHENTICATED":False})
                return self.app(new_env, start_response)

