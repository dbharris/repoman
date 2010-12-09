'''
Created on Oct 5, 2010

@author: fransham
'''
import urllib 
import urllib2
import httplib
import mimetypes, mimetools
import sys
import subprocess
import urlparse
from commands import getstatusoutput
try:
    import json
except:
    import simplejson as json 

HEADERS = {"Content-type":"application/x-www-form-urlencoded", "Accept": "text/plain"}

class repoutils(object):
    
    def post_image_metadata(self, url, repo, cert, key, headers=HEADERS, *args, **kwargs):
        repo_https = self.repo(repo, cert, key)
        params = urllib.urlencode(kwargs['metadata'])
        repo_https.request('POST', '/api/images', params, headers)
        return repo_https.getresponse()

    def update_image_metadata(self, url, repo, cert, key, headers=HEADERS, *args, **kwargs):
        repo_https = self.repo(repo, cert, key)
        params = urllib.urlencode(kwargs['metadata'])
        repo_https.request('POST', '/api/images/'+kwargs['image_name'], params, headers)
        return repo_https.getresponse()
        
    def create_user(self, repo, cert, key, metadata, headers=HEADERS):
        repo_https = self.repo(repo, cert, key)
        params = urllib.urlencode(metadata)
        repo_https.request('POST', '/api/users', params, headers)
        return repo_https.getresponse()
        
    def modify_user(self, repo, cert, key, user, metadata, headers=HEADERS):
        repo_https = self.repo(repo, cert, key)
        params = urllib.urlencode(metadata)
        repo_https.request('POST', '/api/users/'+user, params, headers)
        return repo_https.getresponse()
        
    def modify_group(self, repo, cert, key, group, metadata, headers=HEADERS):
        repo_https = self.repo(repo, cert, key)
        params = urllib.urlencode(metadata)
        repo_https.request('POST', '/api/groups/'+group, params, headers)
        return repo_https.getresponse()
       
    def create_group(self, repo, cert, key, metadata, headers=HEADERS):
        repo_https = self.repo(repo, cert, key)
        params = urllib.urlencode(metadata)
        repo_https.request('POST', '/api/groups', params, headers)
        return repo_https.getresponse()
 
    def get_image_metadata(self, repo, cert, key, image, **kwargs):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('GET', '/api/images/'+image)
        resp = repo_https.getresponse()
        return resp
        
    def get_user_images(self, repo, cert, key, user):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('GET', '/api/users/'+user+'/images')
        resp = repo_https.getresponse()
        return resp
        
    def get_user_images_sharedwith(self, repo, cert, key):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('GET', '/api/users/'+self.get_username(repo, cert, key)+'/shared')
        resp = repo_https.getresponse()
        return resp
        
    def get_user_images_sharedwith_user(self, repo, cert, key, user):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('GET', '/api/users/'+user+'/shared')
        resp = repo_https.getresponse()
        return resp
        
    def get_user_images_sharedwith_group(self, repo, cert, key, group):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('GET', '/api/groups/'+group+'/shared')
        resp = repo_https.getresponse()
        return resp
        
    def delete_image(self, repo, cert, key, name):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('DELETE', '/api/images/'+name)
        resp = repo_https.getresponse()
        return resp

    def share_user(self, repo, cert, key, image, user):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('POST', '/api/images/'+image+'/share/user/'+user)
        resp = repo_https.getresponse()
        return resp

    def share_group(self, repo, cert, key, image, group):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('POST', '/api/images/'+image+'/share/group/'+group)
        resp = repo_https.getresponse()
        return resp

    def unshare_user(self, repo, cert, key, image, user):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('DELETE', '/api/images/'+image+'/share/user/'+user)
        resp = repo_https.getresponse()
        return resp

    def unshare_group(self, repo, cert, key, image, group):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('DELETE', '/api/images/'+image+'/share/group/'+group)
        resp = repo_https.getresponse()
        return resp
        
    def remove_user(self, repo, cert, key, user):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('DELETE', '/api/users/'+user)
        resp = repo_https.getresponse()
        return resp
        
    def remove_group(self, repo, cert, key, group):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('DELETE', '/api/groups/'+group)
        resp = repo_https.getresponse()
        return resp
        
    def remove_image(self, repo, cert, key, image, **kwargs):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('DELETE', '/api/images/'+image)
        resp = repo_https.getresponse()
        return resp
        
    def add_user_to_group(self, repo, cert, key, group, user):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('POST', '/api/groups/'+group+'/users/'+user)
        resp = repo_https.getresponse()
        return resp
        
    def remove_user_from_group(self, repo, cert, key, group, user):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('DELETE', '/api/groups/'+group+'/users/'+user)
        resp = repo_https.getresponse()
        return resp
        
    def add_permission(self, repo, cert, key, group, permission):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('POST', '/api/groups/'+group+'/permissions/'+permission)
        resp = repo_https.getresponse()
        return resp
        
    def remove_permission(self, repo, cert, key, group, permission):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('DELETE', '/api/groups/'+group+'/permissions/'+permission)
        resp = repo_https.getresponse()
        return resp
 
    def repo(self, repo, cert, key):
        hostname = urlparse.urlparse(repo)[1].split(':')[0]
        return httplib.HTTPSConnection(hostname, 443, cert_file=cert, key_file=key)

    def get_images(self,repo,cert,key):
        user = self.get_my_id(repo,cert,key)
        return (user['user_name'],user['images'])
   
    def get_all_images(self,repo,cert,key):
        return self.get_uri_response(repo+"/api/images",cert,key)
 
    def get_users(self,repo,cert,key, *args):
        users =  self.get_uri_response(repo+"/api/users",cert,key)
        if not args[0]:
            return users
        else:
            i=0
            users_info = [0]*len(users)
            for url in users:
                users_info[i] = self.get_uri_response(url,cert,key)
                i = i + 1
            return users_info
            
            
            
    def list_group_members(self,repo,cert,key,group):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('GET', '/api/groups/'+group+'/users')
        resp = repo_https.getresponse()
        return resp
        
    
    def list_groups(self,repo,cert,key):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('GET', '/api/groups')
        resp = repo_https.getresponse()
        return resp
        
    def query_user(self,repo,cert,key,user):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('GET', '/api/users/'+user)
        resp = repo_https.getresponse()
        return resp
        
    def query_group(self,repo,cert,key,group):
        repo_https = self.repo(repo, cert, key)
        repo_https.request('GET', '/api/groups/'+group)
        resp = repo_https.getresponse()
        return resp
            
    
    def get_my_id(self,repo,cert,key):
        ret, output = getstatusoutput("openssl x509 -subject -in "+cert)
        if ret:
            print "Error querying cert with openssl: "
            print output
            sys.exit(1)
        
        my_dn=(output.split('\n')[0])[9:]
        user_data = self.get_users(repo,cert,key, True)
        
        for user in user_data:
            if user['client_dn'] in my_dn:
                return user
                #print user
        return None
    

        
    def get_uri_response(self,uri,cert,key):
        opener = urllib2.build_opener(HTTPSClientAuthHandler(key, cert))
        response = opener.open(uri)
        json_response = json.load(response)
        return json_response

    def get_username(self,repo,cert,key):
        id = self.get_my_id(repo,cert,key)
        return id['user_name']

    def post_image(self,repo,cert,key,imagefile,imagename):
        user_name = self.get_username(repo,cert,key)
        command = "curl -F \"file=@"+imagefile+"\""
        command += " --cert "+cert+" --key "+key+" --insecure "+repo+"/api/images/raw/"+imagename+" > tmpfile"
        p=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        for line in p.stdout.readlines():   
            pass
       
    def download_image(self,repo,cert,key,image,dest):
        command = "curl "+repo+"/api/images/raw/"+image+" -o "+dest+" --cert "+cert+" --key "+key+" --insecure"
        p=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        for line in p.stdout.readlines():
            pass
     
    def get_content_type(filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

class HTTPSClientAuthHandler(urllib2.HTTPSHandler):  
    def __init__(self, key, cert):  
        urllib2.HTTPSHandler.__init__(self)  
        self.key = key  
        self.cert = cert  
    def https_open(self, req): 
        #return self.do_open(self.getConnection, req)
        try:
            return self.do_open(self.getConnection, req)  
        except urllib2.URLError,e:
            if 'error:14094415' in e.reason[1]:
                print "SSL error: your grid proxy certificate appears to be out of date."
                print "Please generate a new proxy with \"grid-proxy-init -rfc\""
                sys.exit(1)
            if 'error:14094418' in e.reason[1]:
                print "SSL error: unknown certificate authority."
                print "Make sure your grid proxy certificate was generated with \"grid-proxy-init -rfc\"."
                print "Also ensure that the repository's Apache server is set to accept proxy certificates (see documentation)"
                sys.exit(1)
            else:
                print "SSL error:" + e.reason[1]
                sys.exit(1)
                 
    def getConnection(self, host, timeout=300):  
        return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)  
    
    
class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable

# Controls how sequences are uncoded. If true, elements may be given multiple values by
#  assigning a sequence.
doseq = 1

    
class MultipartPostHandler(urllib2.BaseHandler):
    handler_order = urllib2.HTTPHandler.handler_order - 10 # needs to run first

    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            v_files = []
            v_vars = []
            try:
                 for(key, value) in data.items():
                     if type(value) == file:
                         v_files.append((key, value))
                     else:
                         v_vars.append((key, value))
            except TypeError:
                systype, value, traceback = sys.exc_info()
                raise TypeError, "not a valid non-string sequence or mapping object", traceback

            if len(v_files) == 0:
                data = urllib.urlencode(v_vars, doseq)
            else:
                boundary, data = self.multipart_encode(v_vars, v_files)
                contenttype = 'multipart/form-data; boundary=%s' % boundary
                if(request.has_header('Content-Type')
                   and request.get_header('Content-Type').find('multipart/form-data') != 0):
                    print "Replacing %s with %s" % (request.get_header('content-type'), 'multipart/form-data')
                request.add_unredirected_header('Content-Type', contenttype)

            request.add_data(data)
        return request

    def multipart_encode(vars, files, boundary = None, buffer = None):
        if boundary is None:
            boundary = mimetools.choose_boundary()
        if buffer is None:
            buffer = ''
        for(key, value) in vars:
            buffer += '--%s\r\n' % boundary
            buffer += 'Content-Disposition: form-data; name="%s"' % key
            buffer += '\r\n\r\n' + value + '\r\n'
        for(key, fd) in files:
            file_size = os.fstat(fd.fileno())[stat.ST_SIZE]
            filename = os.path.basename(fd.name)
            contenttype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            buffer += '--%s\r\n' % boundary
            buffer += 'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (key, filename)
            buffer += 'Content-Type: %s\r\n' % contenttype
            # buffer += 'Content-Length: %s\r\n' % file_size
            fd.seek(0)
            buffer += '\r\n' + fd.read() + '\r\n'
        buffer += '--%s--\r\n\r\n' % boundary
        return boundary, buffer
    multipart_encode = Callable(multipart_encode)

    https_request = http_request

