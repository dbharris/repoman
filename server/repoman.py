#!/usr/bin/env python

import simplejson
import httplib
import urllib

HEADERS = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}

class RepomanError(Exception):
    def __init__(self, e):
        self.e = e

    def __repr__(self):
        return repr(e)


class BadResponse(Exception):
    def __init__(self, resp):
        self.resp = resp

    def __repr__(self):
        return {'status':resp.status, 'reason':resp.reason}


class RepomanClient(object):
    """Client class for connecting to a repoman server.

    Example:
        repo = RepomanClient('repo.server.ca', 443, '/tmp/x509up_u1000')
        repo.connect()
        # Now connected to a repo.server.ca.  Any of the client commands will now work.
    """
    def __init__(self, cert, host, port):
        self.cert = cert
        self.host = host
        self.port = port

    def connect(self):
        self.conn = httplib.HTTPSConnection(host=self.host, port=self.port, cert_file=self.cert)

    def get(self, url):
        try:
            self.conn.request('GET', url)
        except Exception, e:
            raise RepomanError(e)
        else:
            return self.conn.getresponse()

    def post(self, url, params={}, headers=HEADERS):
        try:
            params = urllib.urlencode(params)
            self.conn.request('POST', url, params, headers)
        except Exception, e:
            raise RepomanError(e)
        else:
            return self.conn.getresponse()

    def delete(self, url):
        try:
            self.conn.request('delete', url)
        except Exception, e:
            raise RepomanError(e)
        else:
            return self.conn.getresponse()

    def whoami(self):
        resp = self.get('/api/whoami')
        if resp.status == 200:
            return simplejson.loads(resp.read())
        else:
            raise BadResponse(resp)

    def get_all_users(self):
        resp = self.get('/api/users')
        if resp.status == 200:
            return simplejson.loads(resp.read())
        else:
            raise BadResponse(resp)

    def get_all_images(self):
        resp = self.get('/api/images')
        if resp.status == 200:
            return simplejson.loads(resp.read())
        else:
            raise BadResponse(resp)

    def get_all_groups(self):
        resp = self.get('/api/groups')
        if resp.status == 200:
            return simplejson.loads(resp.read())
        else:
            raise BadResponse(resp)

    def get_user(self, user):
        resp = self.get('/api/users/%s' % user)
        if resp.status == 200:
            return simplejson.loads(resp.read())
        else:
            raise BadResponse(resp)

    def get_image(self, image):
        resp = self.get('/api/images/%s' % image)
        if resp.status == 200:
            return simplejson.loads(resp.read())
        else:
            raise BadResponse(resp)

    def get_group(self, group):
        resp = self.get('/api/groups/%s' % group)
        if resp.status == 200:
            return simplejson.loads(resp.read())
        else:
            raise BadResponse(resp)

    def new_user(self, **kwargs):
        resp = self.post('/api/users', kwargs)
        if resp.status == 200:
            return simplejson.loads(resp.read())
        else:
            raise BadResponse(resp)

    def new_group(self, name,**kwargs):
        resp = self.post('/api/groups', kwargs)
        if resp.status == 200:
            return simplejson.loads(resp.read())
        else:
            raise BadResponse(resp)

    def new_image(self, **kwargs):
        resp = self.post('/api/images', kwargs)
        if resp.status == 201:
            return simplejson.loads(resp.read())
        else:
            raise BadResponse(resp)

    def delete_user(self, name):
        resp = self.delete('/api/users/%s' % user)
        if resp.status == 200:
            return True
        else:
            raise BadResponse(resp)

    def delete_group(self, group):
        resp = self.delete('/api/groups/%s' % group)
        if resp.status == 200:
            return True
        else:
            raise BadResponse(resp)

    def delete_image(self, image):
        resp = self.delete('/api/images/%s' % image)
        if resp.status == 200:
            return True
        else:
            raise BadResponse(resp)

    def modify_user(self, user, **kwargs):
        resp = self.post('/api/users/%s' % user, kwargs)
        if resp.status == 200:
            return simplejson.loads(resp.read())
        else:
            raise BadResponse(resp)

    def modify_image(self, image, **kwargs):
        resp = self.post('/api/images/%s' % image, kwargs)
        if resp.status == 200:
            return simplejson.loads(resp.read())
        else:
            raise BadResponse(resp)

    def modify_group(self, group, **kwargs):
        resp = self.post('/api/groups/%s' % image, kwargs)
        if resp.status == 200:
            return simplejson.loads(resp.read())
        else:
            raise BadResponse(resp)

    def add_user_to_group(self, user, group):
        resp = self.post('/api/groups/%s/users/%s' % (group, user))
        if resp.status == 200:
            return True
        else:
            raise BadResponse(resp)

    def remove_user_from_group(self, user, group):
        resp = self.delete('/api/groups/%s/users/%s' % (group, user))
        if resp.status == 200:
            return True
        else:
            raise BadResponse(resp)

    def add_permission(self, group, permission):
        resp = self.post('/api/groups/%s/permissions/%s' % (group, permission))
        if resp.status == 200:
            return True
        else:
            raise BadResponse(resp)

    def remove_permission(self, group, permission):
        resp = self.delete('/api/groups/%s/permissions/%s' % (group, permission))
        if resp.status == 200:
            return True
        else:
            raise BadResponse(resp)

    def share_with_user(self, image, user):
        resp = self.post('/api/images/%s/share/user/%s' % (image, user))
        if resp.status == 200:
            return True
        else:
            raise BadResponse(resp)

    def unshare_with_user(self, image, user):
        resp = self.delete('/api/images/%s/share/user/%s' % (image, user))
        if resp.status == 200:
            return True
        else:
            raise BadResponse(resp)

    def share_with_group(self, image, group):
        resp = self.post('/api/images/%s/share/group/%s' % (image, group))
        if resp.status == 200:
            return True
        else:
            raise BadResponse(resp)

    def unshare_with_group(self, image, group):
        resp = self.delete('/api/images/%s/share/group/%s' % (image, group))
        if resp.status == 200:
            return True
        else:
            raise BadResponse(resp)

    def upload_raw(self, image, raw):
        url = 'https://' + self.host + ':' + self.port + '/'
        url += '/api/images/raw/%s' % image
        c = pycurl.Curl()
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.HTTPPOST, [('file', (pycurl.FORM_FILE, raw))])
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(pycurl.SSLCERT, self.cert)
        c.perform()
        if c.status == 200:
            return True
        else:
            raise BadResponse(c)

