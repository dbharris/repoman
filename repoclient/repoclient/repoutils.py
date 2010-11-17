'''
Created on Oct 5, 2010

@author: fransham
'''
import urllib 
import urllib2
import httplib
import simplejson as json
from commands import getstatusoutput
import sys

class repoutils(object):
    
    def get_images(self,repo,cert,key):
        user = self.get_user(repo,cert,key)
        return (user['user_name'],user['images'])
    
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
        
        
    def put_image(self,repo,cert,key,imagefile,imagename):
        print "somehow we will upload the image."
        
        
class HTTPSClientAuthHandler(urllib2.HTTPSHandler):  
    def __init__(self, key, cert):  
        urllib2.HTTPSHandler.__init__(self)  
        self.key = key  
        self.cert = cert  
    def https_open(self, req): 
        return self.do_open(self.getConnection, req)  
    def getConnection(self, host, timeout=300):  
        return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)  
   
