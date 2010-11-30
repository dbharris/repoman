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
        repo_https.request('POST', '/api/images/'+kwargs['user_name']+'/'+kwargs['image_name'], params, headers)
        return repo_https.getresponse()
       
 
    def get_image_metadata(self, repo, cert, key, name):
        id = self.get_user(repo,cert,key)
        user_name = id['user_name']
        repo_https = self.repo(repo, cert, key)
        repo_https.request('GET', '/api/images/'+user_name+'/'+name)
        resp = repo_https.getresponse()
        return resp.read()

    def delete_image(self, repo, cert, key, name):
        #id = self.get_user(repo,cert,key)
        #user_name = id['user_name']
        repo_https = self.repo(repo, cert, key)
        repo_https.request('DELETE', '/api/images/'+name)
        resp = repo_https.getresponse()
        return resp.read()

    def share_user(self, repo, cert, key, *args, **kwargs):
        id = self.get_user(repo,cert,key)
        user_name = id['user_name']
        repo_https = self.repo(repo, cert, key)
        repo_https.request('POST', '/api/images/'+user_name+'/'+kwargs['image']+'/share/user/'+kwargs['user'])
        resp = repo_https.getresponse()
        return resp.status

    def share_group(self, repo, cert, key, *args, **kwargs):
        id = self.get_user(repo,cert,key)
        user_name = id['user_name']
        repo_https = self.repo(repo, cert, key)
        repo_https.request('POST', '/api/images/'+user_name+'/'+kwargs['image']+'/share/group/'+kwargs['group'])
        resp = repo_https.getresponse()
        return resp.status

    def unshare_user(self, repo, cert, key, *args, **kwargs):
        id = self.get_user(repo,cert,key)
        user_name = id['user_name']
        repo_https = self.repo(repo, cert, key)
        repo_https.request('DELETE', '/api/images/'+user_name+'/'+kwargs['image']+'/share/user/'+kwargs['user'])
        resp = repo_https.getresponse()
        return resp.status

    def unshare_group(self, repo, cert, key, *args, **kwargs):
        id = self.get_user(repo,cert,key)
        user_name = id['user_name']
        repo_https = self.repo(repo, cert, key)
        repo_https.request('DELETE', '/api/images/'+user_name+'/'+kwargs['image']+'/share/group/'+kwargs['group'])
        resp = repo_https.getresponse()
        return resp.status
 
    def repo(self, repo, cert, key):
        hostname = urlparse.urlparse(repo)[1].split(':')[0]
        return httplib.HTTPSConnection(hostname, 443, cert_file=cert, key_file=key)

    def get_images(self,repo,cert,key):
        user = self.get_user(repo,cert,key)
        return (user['user_name'],user['images'])
   
    def get_all_images(self,repo,cert,key):
        return self.get_uri_response(repo+"/api/images",cert,key)
 
    def get_users(self,repo,cert,key):
        users =  self.get_uri_response(repo+"/api/users",cert,key)
        i=0
        users_info = [0]*len(users)
        for url in users:
            users_info[i] = self.get_uri_response(url,cert,key)
            i = i + 1
        return users_info
    
    def get_my_id(self,repo,cert,key):
        ret, output = getstatusoutput("openssl x509 -subject -in "+cert)
        if ret:
            print "Error querying cert with openssl: "
            print output
            sys.exit(1)
        
        my_dn=(output.split('\n')[0])[9:]
        user_data = self.get_users(repo,cert,key)
        
        for user in user_data:
            if user['client_dn'] in my_dn:
                return user
                #print user
        return None
    
     
    def get_user(self,repo,cert,key):
        myid = self.get_my_id(repo,cert,key)
        return myid
        #return self.get_uri_response(repo+"/api/users/"+str(myid),cert,key)
        
    def get_uri_response(self,uri,cert,key):
        opener = urllib2.build_opener(HTTPSClientAuthHandler(key, cert))
        response = opener.open(uri)
        json_response = json.load(response)
        return json_response

    def get_username(self,repo,cert,key):
        id = self.get_user(repo,cert,key)
        return id['user_name']

    def post_image(self,repo,cert,key,imagefile,imagename):
        user_name = self.get_username(repo,cert,key)
        print "Posting image "+imagefile+" with name "+imagename+" "
        command = "curl -F \"file=@"+imagefile+"\""
        command += " --cert "+cert+" --key "+key+" --insecure "+repo+"/api/images/raw/"+user_name+"/"+imagename+" > tmpfile"
        p=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        for line in p.stdout.readlines():   
            pass
       
    def get_image(self,repo,cert,key,imagename,path):
        user_name = self.get_username(repo,cert,key)
        print "Getting image "+imagename+" and storing it at "+path
        command = "curl -o "+path+imagename+" --cert "+cert+" --key "+key+" --insecure "+repo+"/api/images/raw/"+user_name+"/"+imagename
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
        #except unknown-ca-exception:
        #    print "The server is not accepting your certificate."
        #    print "Ensure your proxy cert is RFC compliant with \"grid-proxy-info\""
        #    print "and ensure that the repoman server's Apache server is set to accept proxy certificates."
        #    sys.exit(1)
        #except:
        #    print "Unknown exception."
        #    sys.exit(1) 
         
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

