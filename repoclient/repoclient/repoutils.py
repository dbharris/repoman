'''
Created on Oct 5, 2010

@author: fransham
'''
import urllib 
import urllib2
import httplib
import mimetypes, mimetools
import simplejson as json
from commands import getstatusoutput
import sys
import subprocess

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

 
    def repo(self, repo, cert, key):
        return httplib.HTTPSConnection('localhost', 443, cert_file=cert, key_file=key)

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
     
    def share_user(self, repo, cert, key, user, image, headers=HEADERS):
        user_name = self.get_username(repo,cert,key)
        repo_https = self.repo(repo, cert, key)
        repo_https.request('POST', '/api/images'+user_name+'/'+image+'/share/user/'+user, headers)
        return repo_https.getresponse()    

    def share_group(self, repo, cert, key, group, image, headers=HEADERS):
        user_name = self.get_username(repo,cert,key)
        repo_https = self.repo(repo, cert, key)
        repo_https.request('POST', '/api/images'+user_name+'/'+image+'/share/group/'+group, headers)
        return repo_https.getresponse()
        

    def get_content_type(filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

class HTTPSClientAuthHandler(urllib2.HTTPSHandler):  
    def __init__(self, key, cert):  
        urllib2.HTTPSHandler.__init__(self)  
        self.key = key  
        self.cert = cert  
    def https_open(self, req): 
        return self.do_open(self.getConnection, req)  
    def getConnection(self, host, timeout=300):  
        return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)  
   
