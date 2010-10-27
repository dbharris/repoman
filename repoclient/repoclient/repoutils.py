'''
Created on Oct 5, 2010

@author: fransham
'''
import urllib 
import urllib2
import httplib
import mimetypes, mimetools
import os, stat
import simplejson as json
from commands import getstatusoutput
import sys
import subprocess

class repoutils(object):
    
    def get_images(self,repo,cert,key):
        user = self.get_user(repo,cert,key)
        return (user['name'],user['images'])
    
    def get_all_images(self,repo,cert,key):
        return self.get_uri_response(repo+"/repository/images",cert,key)
    
    def get_users(self,repo,cert,key):
        return self.get_uri_response(repo+"/repository/users",cert,key)
    
    def get_my_id(self,repo,cert,key):
        ret, output = getstatusoutput("openssl x509 -subject -in "+cert)
        if ret:
            print "Error querying cert with openssl: "
            print output
            sys.exit(1)
        
        my_dn=(output.split('\n')[0])[9:] 
        user_data = self.get_users(repo,cert,key)
        if user_data['client_dn']==my_dn:
            return user_data['uuid']
        return None
    
     
    def get_user(self,repo,cert,key):
        myid = self.get_my_id(repo,cert,key)
        return self.get_uri_response(repo+"/repository/users/"+str(myid),cert,key)
        
    def get_uri_response(self,uri,cert,key):
        opener = urllib2.build_opener(HTTPSClientAuthHandler(key, cert))
        response = opener.open(uri)
        return json.load(response)
        
        
    def post_image(self,repo,cert,key,imagefile,imagename):
        command = 'curl -F "file=@'+imagefile+'" -F "name='+imagename
        command += '" --cert '+cert+' --key '+key+' --insecure '+repo
        command +=    '/repository/images > tmpfile'
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
        return self.do_open(self.getConnection, req)  
    def getConnection(self, host, timeout=300):  
        return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert) 