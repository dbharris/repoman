#!/usr/bin/env python

import simplejson
import httplib
import urllib
from os import getuid

HEADERS = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}

DEFAULT_CLI_CONFIG = {}

DEFAULT_CLIENT_CONFIG = {'host':'localhost',
                         'port':443,
                         'cert':'/tmp/x509up_u%s' % getuid()}

class RepomanError(Exception):
    def __init__(self, e):
        self.e = e

    def __repr__(self):
        return repr(e)


class BadResponse(Exception):
    def __init__(self, resp):
        self.resp = resp

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return repr({'status':self.resp.status, 'reason':self.resp.reason,
                      'response':self.resp.read()})


class RepomanClient(object):
    """Client class for connecting to a repoman server.

    Example:
        repo = RepomanClient('repo.server.ca', 443, '/tmp/x509up_u1000')
        # Now connected to a repo.server.ca.  Any of the client commands will now work.
    """
    def __init__(self, cert, host, port):
        self.cert = cert
        self.host = host
        self.port = port

        self._connect()

    def _connect(self):
        self.conn = httplib.HTTPSConnection(host=self.host, port=self.port, cert_file=self.cert)

        (user, resp) = self.whoami()
        self.user_name = user['user_name']

    def _get(self, url):
        try:
            self.conn.request('GET', url)
        except Exception, e:
            raise RepomanError(e)
        else:
            return self.conn.getresponse()

    def _post(self, url, params={}, headers=HEADERS):
        try:
            params = urllib.urlencode(params)
            self.conn.request('POST', url, params, headers)
        except Exception, e:
            raise RepomanError(e)
        else:
            return self.conn.getresponse()

    def _delete(self, url):
        try:
            self.conn.request('DELETE', url)
        except Exception, e:
            raise RepomanError(e)
        else:
            return self.conn.getresponse()

    def whoami(self):
        resp = self._get('/api/whoami')
        if resp.status == 200:
            return simplejson.loads(resp.read()), resp
        else:
            raise BadResponse(resp)

    def get_all_users(self):
        resp = self._get('/api/users')
        if resp.status == 200:
            return simplejson.loads(resp.read()), resp
        else:
            raise BadResponse(resp)

    def get_all_images(self):
        resp = self._get('/api/images')
        if resp.status == 200:
            return simplejson.loads(resp.read()), resp
        else:
            raise BadResponse(resp)

    def get_all_groups(self):
        resp = self._get('/api/groups')
        if resp.status == 200:
            return simplejson.loads(resp.read()), resp
        else:
            raise BadResponse(resp)

    def get_user_images(self, user):
        resp = self._get('/api/users/%s/images' % user)
        if resp.status == 200:
            return simplejson.loads(resp.read()), resp
        else:
            raise BadResponse(resp)

    def get_my_images(self):
        return self.get_user_images(self.user_name)

    def get_images_shared_with_user(self, user):
        resp = self._get('/api/users/%s/shared' % user)
        if resp.status == 200:
            return simplejson.loads(resp.read()), resp
        else:
            raise BadResponse(resp)

    def get_images_shared_with_me(self):
        return self.get_images_shared_with_user(self.user_name)

    def get_images_shared_by_me(self):
        resp = self._get('/api/users/%s/sharing' % self.user_name)
        if resp.status == 200:
            return simplejson.loads(resp.read()), resp
        else:
            raise BadResponse(resp)

    def get_user(self, user):
        resp = self._get('/api/users/%s' % user)
        if resp.status == 200:
            return simplejson.loads(resp.read()), resp
        else:
            raise BadResponse(resp)

    def get_image(self, image):
        resp = self._get('/api/images/%s' % image)
        if resp.status == 200:
            return simplejson.loads(resp.read()), resp
        else:
            raise BadResponse(resp)

    def get_group(self, group):
        resp = self._get('/api/groups/%s' % group)
        if resp.status == 200:
            return simplejson.loads(resp.read()), resp
        else:
            raise BadResponse(resp)

    def new_user(self, **kwargs):
        print kwargs
        resp = self._post('/api/users', kwargs)
        if resp.status == 200:
            return simplejson.loads(resp.read()), resp
        else:
            raise BadResponse(resp)

    def new_group(self, name,**kwargs):
        resp = self._post('/api/groups', kwargs)
        if resp.status == 200:
            return simplejson.loads(resp.read()), resp
        else:
            raise BadResponse(resp)

    def new_image(self, **kwargs):
        resp = self._post('/api/images', kwargs)
        if resp.status == 201:
            return simplejson.loads(resp.read()), resp
        else:
            raise BadResponse(resp)

    def delete_user(self, name):
        resp = self._delete('/api/users/%s' % user)
        if resp.status == 200:
            return True, resp
        else:
            raise BadResponse(resp)

    def delete_group(self, group):
        resp = self._delete('/api/groups/%s' % group)
        if resp.status == 200:
            return True, resp
        else:
            raise BadResponse(resp)

    def delete_image(self, image):
        resp = self._delete('/api/images/%s' % image)
        if resp.status == 200:
            return True, resp
        else:
            raise BadResponse(resp)

    def modify_user(self, user, **kwargs):
        resp = self._post('/api/users/%s' % user, kwargs)
        if resp.status == 200:
            return True, resp
        else:
            raise BadResponse(resp)

    def modify_image(self, image, **kwargs):
        resp = self._post('/api/images/%s' % image, kwargs)
        if resp.status == 200:
            return True, resp
        else:
            raise BadResponse(resp)

    def modify_group(self, group, **kwargs):
        resp = self._post('/api/groups/%s' % group, kwargs)
        if resp.status == 200:
            return True, resp
        else:
            raise BadResponse(resp)

    def add_user_to_group(self, user, group):
        resp = self._post('/api/groups/%s/users/%s' % (group, user))
        if resp.status == 200:
            return True, resp
        else:
            raise BadResponse(resp)

    def remove_user_from_group(self, user, group):
        resp = self._delete('/api/groups/%s/users/%s' % (group, user))
        if resp.status == 200:
            return True, resp
        else:
            raise BadResponse(resp)

    def add_permission(self, group, permission):
        resp = self._post('/api/groups/%s/permissions/%s' % (group, permission))
        if resp.status == 200:
            return True, resp
        else:
            raise BadResponse(resp)

    def remove_permission(self, group, permission):
        resp = self._delete('/api/groups/%s/permissions/%s' % (group, permission))
        if resp.status == 200:
            return True, resp
        else:
            raise BadResponse(resp)

    def share_with_user(self, image, user):
        resp = self._post('/api/images/%s/share/user/%s' % (image, user))
        if resp.status == 200:
            return True, resp
        else:
            raise BadResponse(resp)

    def unshare_with_user(self, image, user):
        print '/api/images/%s/share/user/%s' % (image, user)
        resp = self._delete('/api/images/%s/share/user/%s' % (image, user))
        if resp.status == 200:
            return True, resp
        else:
            raise BadResponse(resp)

    def share_with_group(self, image, group):
        resp = self._post('/api/images/%s/share/group/%s' % (image, group))
        if resp.status == 200:
            return True, resp
        else:
            raise BadResponse(resp)

    def unshare_with_group(self, image, group):
        resp = self._delete('/api/images/%s/share/group/%s' % (image, group))
        if resp.status == 200:
            return True, resp
        else:
            raise BadResponse(resp)

    def upload_raw(self, image, raw):
        import pycurl

        url = 'https://' + self.host + ':' + str(self.port)
        url += '/api/images/raw/%s' % image
        c = pycurl.Curl()
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.HTTPPOST, [('file', (pycurl.FORM_FILE, raw))])
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(pycurl.SSLCERT, self.cert)
        try:
            c.perform()
            return True
        except:
            raise BadResponse(c)


class RepomanCLI(object):
    def __init__(self):
        pass

    def make_parser(self):
        pass

