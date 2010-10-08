# query a url


# add a new user
    import httplib
    import urllib

    repo = httplib.HTTPSConnection('localhost', 4444, cert_file='/tmp/x509up_u1000')
    headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    params = urllib.urlencode({'name':"TESter", 'email':'test22@test.ca', 'client_dn':'blah balh', 'global_admin':False, 'suspended':False})
    repo.request('POST', '/repository/users', params, headers)
    resp = repo.getresponse()

# add a new group


# add a new image
    import pycurl
    c = pycurl.Curl()
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.URL, 'https://localhost:4444/repository/images')
    c.setopt(pycurl.HTTPPOST, [('file', (pycurl.FORM_FILE, '/tmp/vm_image.img')), ('name', 'test_image')])
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSLCERT, '/tmp/x509up_u1000')
    c.perform()