

import httplib
import urllib
import random
import pycurl


SERVER = 'localhost'
PORT = 4444
CERT = '/tmp/x509up_u1000'

def print_resp(resp):
    print "STATUS: %d" % resp.status
    print "REASON: %s" % resp.reason
    print "----------------------------"
    print "MESSAGE: %s" % resp.read()


def new_group(name):
    repo = httplib.HTTPSConnection(SERVER, PORT, cert_file=CERT)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode({'name':name})
    repo.request('POST', '/api/groups', params, headers)
    resp = repo.getresponse()
    print_resp(resp)

def new_user(name):
    dn = str(random.randrange(1000000, 9999999))
    repo = httplib.HTTPSConnection(SERVER, PORT, cert_file=CERT)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode({'user_name':name, 'full_name':name,
                               'cert_dn':dn, 'email':name+'@email.com'})
    repo.request('POST', '/api/users', params, headers)
    resp = repo.getresponse()
    print_resp(resp)

def new_image(**kwargs):
    repo = httplib.HTTPSConnection(SERVER, PORT, cert_file=CERT)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode(kwargs)
    repo.request('POST', '/api/images', params, headers)
    resp = repo.getresponse()
    print_resp(resp)


def delete_user(name):
    repo = httplib.HTTPSConnection(SERVER, PORT, cert_file=CERT)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode({})
    repo.request('DELETE', '/api/users/'+name, params, headers)
    resp = repo.getresponse()
    print_resp(resp)

def delete_group(name):
    repo = httplib.HTTPSConnection(SERVER, PORT, cert_file=CERT)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode({})
    repo.request('DELETE', '/api/groups/'+name, params, headers)
    resp = repo.getresponse()
    print_resp(resp)

def add_user_to_group(group, user):
    repo = httplib.HTTPSConnection(SERVER, PORT, cert_file=CERT)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode({})
    repo.request('POST', '/api/groups/'+group+'/users/'+user, params, headers)
    resp = repo.getresponse()
    print_resp(resp)

def remove_user_from_group(group, user):
    repo = httplib.HTTPSConnection(SERVER, PORT, cert_file=CERT)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode({})
    repo.request('DELETE', '/api/groups/'+group+'/users/'+user, params, headers)
    resp = repo.getresponse()
    print_resp(resp)

def add_permission(group, permission):
    repo = httplib.HTTPSConnection(SERVER, PORT, cert_file=CERT)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode({})
    repo.request('POST', '/api/groups/'+group+'/permissions/'+permission, params, headers)
    resp = repo.getresponse()
    print_resp(resp)

def remove_permission(group, permission):
    repo = httplib.HTTPSConnection(SERVER, PORT, cert_file=CERT)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode({})
    repo.request('DELETE', '/api/groups/'+group+'/permissions/'+permission, params, headers)
    resp = repo.getresponse()
    print_resp(resp)

def share_with_user(image_user, image, user=None):
    repo = httplib.HTTPSConnection(SERVER, PORT, cert_file=CERT)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode({})
    repo.request('POST', '/api/images/'+image_user+'/'+image+'/share/user/'+user, params, headers)
    resp = repo.getresponse()
    print_resp(resp)

def share_with_group(image_user, image, group=None):
    repo = httplib.HTTPSConnection(SERVER, PORT, cert_file=CERT)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode({})
    repo.request('POST', '/api/images/'+image_user+'/'+image+'/share/group/'+group, params, headers)
    resp = repo.getresponse()
    print_resp(resp)

def unshare_with_user(image_user, image, user=None):
    repo = httplib.HTTPSConnection(SERVER, PORT, cert_file=CERT)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode({})
    repo.request('DELETE', '/api/images/'+image_user+'/'+image+'/share/user/'+user, params, headers)
    resp = repo.getresponse()
    print_resp(resp)

def unshare_with_group(image_user, image, group=None):
    repo = httplib.HTTPSConnection(SERVER, PORT, cert_file=CERT)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode({})
    repo.request('DELETE', '/api/images/'+image_user+'/'+image+'/share/group/'+group, params, headers)
    resp = repo.getresponse()
    print_resp(resp)

def modify_image(user, image, **kwargs):
    repo = httplib.HTTPSConnection(SERVER, PORT, cert_file=CERT)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode(kwargs)
    repo.request('POST', '/api/images/'+user+'/'+image, params, headers)
    resp = repo.getresponse()
    print_resp(resp)

def modify_user(user, **kwargs):
    repo = httplib.HTTPSConnection(SERVER, PORT, cert_file=CERT)
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode(kwargs)
    repo.request('POST', '/api/users/'+user, params, headers)
    resp = repo.getresponse()
    print_resp(resp)

def upload_raw(path, user, image):
    c = pycurl.Curl()
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.URL, 'https://%s:%d/api/images/raw/%s/%s' % (SERVER, PORT, user, image))
    c.setopt(pycurl.HTTPPOST, [('file', (pycurl.FORM_FILE, path))])
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSLCERT, CERT)
    c.perform()

