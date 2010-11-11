# How-to
This is a quick and dirty description of how to perform different actions on repoman.


## Assumptions
The following python modules are imported and available in the current namespace.

    import httplib
    import urllib
    import pycurl       # only needed for uploading a file

The following objects are available in the current namespace.

    # replace HOST, PORT according to your install
    # replace YOUR_PROXY_CERT with the path to your proxy cert. (ie. /tmp/x509up_u1000)
    repo = httplib.HTTPSConnection(HOST, PORT, cert_file=YOUR_PROXY_CERT)

Long line in code output have been manually wrapped.

## Get a list of users
    >>> repo.request('GET', '/api/users')
    >>> resp = repo.getresponse()
    >>> resp.read()
    """["https://localhost:4444/api/users/doug", "https://localhost:4444/api/users/bob"]"""

## Examine a specific user
    >>> repo.request('GET', '/api/users/bob')
    >>> resp = repo.getresponse()
    >>> resp.read()
    """{"groups": ["https://localhost:4444/api/groups/users"], "full_name": "bob",\
    "client_dn": "6317825", "suspended": false, "images": [], "user_name": "bob",\
    "email": "bob@email.com", "permissions": ["image_delete_owned", "image_create_owned",\
    "user_modify_self", "image_modify_owned"]}"""

## Examine a specific image
    >>> repo.request('GET', '/api/images/bob/test_image.gz')
    >>> resp = repo.getresponse()
    >>> resp.read()
    """{"uploaded": "Thu Nov 11 00:04:59 2010", "read_only": true, "uuid": "52c568b5ed2711df99b30026b9545de1",\
    "raw_file_uploaded": false, "shared_with": {"users": [], "groups": []},\
    "checksum": {"type": null, "value": null}, "os_variant": null, "expires": null,\
    "file_url": "https://localhost:4444/api/images/raw/bob/test_img.gz",\
    "modified": "Thu Nov 11 00:04:59 2010", "os_arch": null, "allow_http_get": false,\
    "description": "A test image compressed with gzip", "owner_user_name": "bob",\
    "version": 0, "hypervisor": null, "owner": "https://localhost:4444/api/users/bob",\
    "os_type": null, "http_file_url": null, "name": "test_img.gz"}


## add a new group
    >>> headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    >>> params = urllib.urlencode({'name':'new_group_name'})
    >>> repo.request('POST', '/api/groups', params, headers)
    >>> resp = repo.getresponse()


## Create an Image and upload the image file
### Creating the image
    >>> headers = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}
    >>> params = urllib.urlencode({'name':'My_test_image.raw.gz', 'description':"The Most Amazing Image Ever!",
    ... 'os_arch':'x86_64', 'os_variant':'rhel 5.5', 'hypervisor':'kvm'})
    >>> repo.request('POST', '/api/images', params, headers)
    >>> resp = repo.getresponse()
    >>> resp.status
    201
    >>> resp.getheader('location')
    'https://localhost:4444/api/raw/bob/My_test_image.raw.gz'

**Note that the image object contains a flag `raw_file_uploaded` that will remain false until the image file is uploaded**
**Attempting to perform a GET on the raw image url will result in a "404 - Not Found" error**

### Upload the corresponding image file
    c = pycurl.Curl()
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.URL, 'https://localhost:4444/api/images/raw/bob/My_test_image.raw.gz')
    c.setopt(pycurl.HTTPPOST, [('file', (pycurl.FORM_FILE, '/tmp/vm_image.img'))])
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSLCERT, '/tmp/x509up_u1000')
    c.perform()

