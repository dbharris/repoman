# query a url
    import httplib

    repo = httplib.HTTPSConnection('localhost', 4444, cert_file='/tmp/x509up_u1000')
    repo.request('GET', '/repository/users')
    resp = repo.getresponse()

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
    
    class ResponseHeaders(object):
        def __init__(self):
            self.headers = []
        
        def store(self, buff):
            self.headers.append(buff)
            
        def __repr__(self):
            return repr(self.headers)
    
    # upload the metadata for the image
    response_headers = ResponseHeaders()
    c = pycurl.Curl()
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.URL, 'https://localhost:4444/api/images/meta')
    c.setopt(pycurl.HTTPPOST, [('name', 'test_image'), ('desc', 'Some human description')])
    c.setopt(c.HEADERFUNCTION, response_headers.store)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSLCERT, '/tmp/x509up_u1000')
    c.perform()
    
    # The response from the server will be a '201' code.  The 'Location:' header
    # will contain the url to post the raw file to, or just post it to 
    # /api/images/raw/{UUID}
    
    # upload the corresponding raw image
    c = pycurl.Curl()
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.URL, 'https://localhost:4444/api/images/raw/{uuid}')
    c.setopt(pycurl.HTTPPOST, [('file', (pycurl.FORM_FILE, '/tmp/vm_image.img'))])
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSLCERT, '/tmp/x509up_u1000')
    c.perform()
    
    # once the raw file has been posted, the database will be 
