'''
Created on Oct 5, 2010

@author: fransham
'''

import ConfigParser
import imageutils,repoutils
import sys,os
from commands import getstatusoutput
import pprint
#write help


class repoclient(object):

    def __init__(self):
        self.read_config_file()
        self.iut = imageutils.imageutils()
        self.rut = repoutils.repoutils()
    
        
    def read_config_file(self):
        
        config = ConfigParser.RawConfigParser()
        config.read("/etc/repoclient/repoclient.conf")

        # read in some values that MUST be set:
        try:
            self.imagepath=config.get("ThisImage","image")
            self.mountpoint=config.get("ThisImage","mountpoint")
        except ConfigParser.NoSectionError:
            print "Trouble reading config file. (/etc/repoclient/repoclient.conf"  
            print "Make sure a mountpoint and image file are specified"
            sys.exit(1)
    
        try:
            self.imagename=config.get("ThisImage","imagename")
            self.repository=config.get("ThisImage","repository")
        except ConfigParser.NoSectionError:
            print "Trouble reading config file. (/etc/repoclient/repoclient.conf"  
            print "Make sure an imagename and repository are specified"
            sys.exit(1)
            
        try:
            self.usercert=config.get("ThisImage","usercert")
            self.userkey=config.get("ThisImage","userkey")
        except ConfigParser.NoSectionError:
            print "Trouble reading config file. (/etc/repoclient/repoclient.conf"  
            print "Make sure a usercert and userkey are specified"
            sys.exit(1)
        if not (os.path.exists(self.usercert) or os.path.exists(self.userkey)):
            print "Your certificate and/or key doesn't exist as specified in"
            print "/etc/repoclient/repoclient.conf.  exiting."
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
                
    def get_user(self, getuid=0):
        me = self.rut.get_user(self.repository, self.usercert, self.userkey, uid=getuid)
        print '\n'
        for key in me:
            print "  "+key+": \t",
            print me[key]
        print '\n'
    
    def list_users(self):
        users = self.rut.get_users(self.repository, self.usercert, self.userkey)
        print '\n'
        for user in users:
            print "  "+user+": \t",
            print users[user]
        print '\n'
    
    def list_images(self,getuid=0):
        images = self.rut.get_images(self.repository, self.usercert, self.userkey, uid=getuid)
        print '\n    Images for user: '+images[0]+':\n'
        for image in images[1]:
            print "      ",
            print image
        print '\n'
        
        
    def save_image(self, imagename):
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
        self.rut.put_image(self.repository,self.usercert,self.userkey, self.imagepath,imagename)
        
        print '\n   Image successfully uploaded to  the repository at:\n    '
        print self.repository
    
    def list_all_images(self):
        print self.rut.get_all_images(self.repository, self.usercert, self.userkey)   
        
          
    def post_image(self,imagename):  
        self.rut.post_image(self.repository,self.usercert,self.userkey, self.imagepath,imagename,"a911ff8c547443628b19e5bfbaa3b6da")     
        