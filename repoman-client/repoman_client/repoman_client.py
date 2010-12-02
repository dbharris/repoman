'''
Created on Oct 5, 2010

@author: fransham, dbharris
'''

import ConfigParser
import imageutils,repoutils
import sys,os
from commands import getstatusoutput
import pprint
import os.path

try:
    import json
except:
    import simplejson as json
#write help


class repoman_client(object):

    def __init__(self):
        self.read_config_file()
        self.iut = imageutils.imageutils()
        self.rut = repoutils.repoutils()
    
        
    def read_config_file(self):
        config = ConfigParser.RawConfigParser()
        user_config = os.getenv("HOME")+'/.repoman-client'
        if os.path.isfile(os.getenv("HOME")+'/.repoman-client'):
            config.read(os.getenv("HOME")+'/.repoman-client')
        else:
            config.read('/etc/repoman-client/repoman-client.conf')

        # read in some values that MUST be set:
        try:
            self.imagepath=config.get("ThisImage","image")
            self.mountpoint=config.get("ThisImage","mountpoint")
        except ConfigParser.NoSectionError:
            print "Trouble reading config file."  
            print "Make sure a mountpoint and image file are specified in the config"
            print "(either /etc/repoman-client/repoman-client.conf or ~/.repoman-client)"
            sys.exit(1)
    
        try:
            self.imagename=config.get("ThisImage","imagename")
            self.repository=config.get("ThisImage","repository")
        except ConfigParser.NoSectionError:
            print "Trouble reading config file."  
            print "Make sure an imagename and repository are specified in the config"
            print "(either /etc/repoman-client/repoman-client.conf or ~/.repoman-client)"
            sys.exit(1)
        
        #attempt to define the usercert/userkey based on default grid-proxy-init values    
        self.usercert='/tmp/x509up_u%s' % str(os.geteuid())
        self.userkey='/tmp/x509up_u%s' % str(os.geteuid())
        if not os.path.exists(self.usercert):
            print 'Could not find a proxy cert at /tmp/x509up_u%s' % str(os.geteuid())
            print 'Searching for a valid certificate location in the configuration file.'
            try:
                self.usercert=config.get("ThisImage","usercert")
                self.userkey=config.get("ThisImage","userkey")
            except ConfigParser.NoOptionError:
                print "Could not find a certificate in the configuration file."  
                print "Please either use grid-proxy-init to generate a new proxy cert or specify an alternate certifate in the configuration file."
                print "(either /etc/repoman-client/repoman-client.conf or ~/.repoman-client)"
                sys.exit(1)
            except ConfigParser.NoSectionError:
                print "Could not find a certificate in the configuration file."
                print "Please either use grid-proxy-init to generate a new proxy cert or specify an alternate certifate in the configuration file."
                print "(either /etc/repoman-client/repoman-client.conf or ~/.repoman-client)"
                sys.exit(1)
            if not (os.path.exists(self.usercert) or os.path.exists(self.userkey)):
                print "Your certificate and/or key doesn't exist as specified in"
                print "the config file."
                print "(either /etc/repoman-client/repoman-client.conf or ~/.repoman-client)"
                sys.exit(1)    
        
        
        #these values are optional, and are set if they don't exist
        try:
            self.lockfile=config.get("ThisImage","lockfile")
        except ConfigParser.NoOptionError:
            self.lockfile="/var/lock/reposync.pid"
    
        try:
            self.sync_onboot=config.getboolean("ThisImage","sync_onboot")
        except ConfigParser.Error:
            self.sync_onboot = True
        
        try:
            self.excl_dirs=config.get("ThisImage","exclude_dirs") + self.mountpoint
        except ConfigParser.NoOptionError:
            self.excl_dirs = self.mountpoint
                       
    
    def create_image(self):        
        self.iut.create_image(self.imagepath)
        self.iut.mount_image(self.imagepath,self.mountpoint)
        if not self.iut.check_mounted(self.imagepath,self.mountpoint):
            print "File is not mounted.  Check that you have the proper permissions to run this command"
            sys.exit(1)
        
    
    def sync_is_running(self):
        if os.path.exists(self.lockfile):
            print self.lockfile
            return True
        return False
    
    def create_local_bundle(self):
        if self.sync_is_running():
            pid=open(self.lockfile,'r').read()
            print "The local image creation is already in progress... speeding it up"
            print "This can take some time... please wait."
            print "If you're sure this is an error, cancel this script and delete: "
            print "  "+self.lockfile
            os.system("renice -19 "+pid);
            os.waitpid(int(pid),0)
            print "Local image copy created"
        else:
            pid = os.getpid()
            lf = open(self.lockfile,'w')
            lf.write(str(pid))
            lf.close()
            try:
                self.create_image()
                self.iut.sync_filesystem(self.mountpoint, self.excl_dirs)
                os.remove(self.lockfile)
            except imageutils.MountError,e:
                print e.msg
                os.remove(self.lockfile)
                sys.exit(1)
                
    def get_user(self):
        user = self.rut.get_user(self.repository, self.usercert, self.userkey)
        print '\n'
        for key in user:
            if key == 'images':
                print "  "+key+":"
                for image in user['images']:
                    print "  "+image
            else:
                print "  "+key+": \t",
                print user[key]
        print '\n'
 
    def list_users(self):
        users = self.rut.get_users(self.repository, self.usercert, self.userkey)
        print '\n'
        for user in users:
            print '\n'
            for key in user:
                if key == 'images':
                    print "  "+key+":"
                    for image in user['images']:
                        print "  "+image
                else:
                    print "  "+key+": \t",
                    print user[key]
        print '\n'
    
    def list_user_images(self, user, *args):
        images = json.loads(self.rut.get_user_images(self.repository, self.usercert, self.userkey, user))
        if args[0]:
            print "Images for user "+user+":"
            for image in images:
                print image
        else:
            print "Images for user "+user+":"
            for image in images:
                print image.split('/')[6]
    
    
    
    def list_images(self, *args):
        if args[0]:
            images = self.rut.get_images(self.repository, self.usercert, self.userkey)
            print 'Images for user '+images[0]+':'
            for image in images[1]:
                print image
        else:
            images = self.rut.get_images(self.repository, self.usercert, self.userkey)
            print 'Images for user '+images[0]+':'
            for image in images[1]:
                print image.split('/')[6]
            


    def list_images_raw(self):
        images = self.rut.get_images(self.repository, self.usercert, self.userkey)
        return images[1]

    def new_image(self, *args, **kwargs):
        metadata = kwargs['metadata']
        resp = self.rut.post_image_metadata('/api/images', self.repository, self.usercert, self.userkey, metadata=metadata)
        if kwargs['replace']:
            print "Updating metadata."
            resp = self.rut.update_image_metadata('/api/images', self.repository, self.usercert, self.userkey, user_name=self.rut.get_username(self.repository,self.usercert,self.userkey), image_name=metadata['name'], metadata=metadata)
            if resp.status == 200:
                print "Metadata modification complete."
            else:
                print "Metadata was not modified: "+str(resp.status)
        else:
            if resp.status == 201:
                print "Metadata uploaded, image created."
            else:
                print "Image was not created: response code "+str(resp.status)

    def update_metadata(self, *args, **kwargs):
        metadata = kwargs['metadata']
        exists = kwargs['exists']
        self.new_image(metadata=metadata, replace=exists)
        

    def get_image_info(self, name):
        resp = self.rut.get_image_metadata(self.repository, self.usercert, self.userkey, name)
        
        json_resp = json.loads(resp)
        return json_resp

    def delete(self, name):
        resp = self.rut.delete_image(self.repository, self.usercert, self.userkey, name)
        if not str(resp):
            print "Image "+name+" deleted."



    def save_image(self, *args, **kwargs):
        metadata = kwargs['metadata']
        print "Posting new image metadata to the repository."
        if kwargs['replace']:
            print "Replacing existing image "+metadata['name']
        else:
            print "Creating new image on repository with name "+metadata['name']
        self.new_image(metadata=metadata,replace=kwargs['replace'])
    
        print '''
        
    Creating an image of the local filesystem.  
    This can take up to 10 minutes or more
    Please be patient ...
    test
        '''
        if not self.iut.check_mounted(self.imagepath, self.mountpoint):
            print "Creating a new image:"
            os.system("rm -rf "+self.imagepath+" "+self.mountpoint)
            self.create_local_bundle()  
        elif self.sync_is_running():
            print "Sync is already running...what?"
            self.create_local_bundle()
        else:
            print "syncing image"
            self.iut.sync_filesystem(self.mountpoint, self.excl_dirs)
            
        print '''
        
    Local copy of filesystem created.  Uploading
    to the image repository.  This can also take 
    time, depending on the speed of your connection
    and the size of your image...
        '''
        self.rut.post_image(self.repository,self.usercert,self.userkey, self.imagepath,metadata['name'])
        
        print '\n   Image successfully uploaded to  the repository at:\n    '
        print self.repository
    
    def upload_image(self, file, *args, **kwargs):
        metadata = kwargs['metadata']
        name = kwargs['name']
        print "Uploading image "+file+" to repository "+self.repository+" with name "+name
        print "Posting new image metadata to the repository."
        if kwargs['replace']:
            print "Replacing existing image "+metadata['name']
        else:
            print "Creating new image on repository with name "+metadata['name']
        self.new_image(metadata=metadata,replace=kwargs['replace'])

        self.rut.post_image(self.repository,self.usercert,self.userkey,file,name)
     
    def list_all_images(self):
        image_list = self.rut.get_all_images(self.repository, self.usercert, self.userkey)
        for item in image_list:
            print item
        
          
    def post_image(self,imagename):  
        self.rut.post_image(self.repository,self.usercert,self.userkey, self.imagepath,imagename)


    def share_user(self, *args, **kwargs):
        print "Sharing file "+kwargs['image']+"with user "+kwargs['user']
        resp = self.rut.share_user(self.repository, self.usercert, self.userkey, user=kwargs['user'], image=kwargs['image']) 
        if resp == 200:
            print "Share complete."
        else:
            print "Share failed: HTTP code "+str(resp)

    def share_group(self, *args, **kwargs):
        print "Sharing file "+kwargs['image']+"with group "+kwargs['group']
        resp = self.rut.share_group(self.repository, self.usercert, self.userkey, group=kwargs['group'], image=kwargs['image']) 
        if resp == 200:
            print "Share complete."
        else:
            print "Share failed: HTTP code "+str(resp)

    def unshare_user(self, *args, **kwargs):
        print "Unsharing file "+kwargs['image']+"with user "+kwargs['user']
        resp = self.rut.unshare_user(self.repository, self.usercert, self.userkey, user=kwargs['user'], image=kwargs['image']) 
        if resp == 200:
            print "Unshare complete."
        else:
            print "Unshare failed: HTTP code "+str(resp)

    def unshare_group(self, *args, **kwargs):
        print "Unsharing file "+kwargs['image']+"with group "+kwargs['group']
        resp = self.rut.unshare_group(self.repository, self.usercert, self.userkey, group=kwargs['group'],  image=kwargs['image'])
        if resp == 200:
            print "Unshare complete."
        else:
            print "Unshare failed: HTTP code "+str(resp)
    
    def get(self, *args, **kwargs):
        try:
            path = kwargs['path']
        except:
            path = './'
        imagename = kwargs['name']
        resp = self.get_image_info(imagename)
        if resp['raw_file_uploaded']:
            self.rut.get_image(self.repository,self.usercert,self.userkey,imagename,path)
        else:
            print "The raw image for "+imagename+" has not been uploaded yet."

