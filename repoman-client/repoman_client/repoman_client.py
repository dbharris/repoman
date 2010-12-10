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
        env_config = os.getenv("REPOMAN_CLIENT_CONFIG")
        if env_config:
            if os.path.isfile(env_config):
                config.read(env_config)
        else:
            if os.path.isfile(os.getenv("HOME")+'/.repoman-client'):
                config.read(os.getenv("HOME")+'/.repoman-client')
            else:
                print "Could not find a configuration file in ~/.repoman-client or in the path specified by the the environment variable \"REPOMAN_CLIENT_CONFIG\""
                print "Please run 'repoman make-config' or specify a custom configfile by exporting its location as REPOMAN_CLIENT_CONFIG."
                sys.exit(1)


        # read in some values that MUST be set:
        try:
            self.imagepath=os.path.expanduser(config.get("ThisImage","image"))
            self.mountpoint=os.path.expanduser(config.get("ThisImage","mountpoint"))
        except ConfigParser.NoSectionError:
            print "Trouble reading config file."  
            print "Make sure a mountpoint and image file are specified in the config"
            print "(either ~/.repoman-client)"
            sys.exit(1)
    
        try:
            self.repository=config.get("ThisImage","repository")
        except ConfigParser.NoSectionError:
            print "Trouble reading config file."  
            print "Make sure a repository is specified in the config"
            print "(either ~/.repoman-client)"
            sys.exit(1)
        
        #attempt to define the usercert/userkey based on default grid-proxy-init values    
        self.usercert='/tmp/x509up_u%s' % str(os.geteuid())
        self.userkey='/tmp/x509up_u%s' % str(os.geteuid())
        if not os.path.exists(self.usercert):
            try:
                self.usercert=os.path.expanduser(config.get("ThisImage","usercert"))
                self.userkey=os.path.expanduser(config.get("ThisImage","userkey"))
            except ConfigParser.NoOptionError:
                print "Could not find a certificate in the configuration file or at /tmp/x509up_u%USERID%."  
                print "Please either use grid-proxy-init to generate a new proxy cert or specify an alternate certifate in the configuration file."
                print "(either ~/.repoman-client)"
                sys.exit(1)
            except ConfigParser.NoSectionError:
                print "Could not find a certificate in the configuration file."
                print "Please either use grid-proxy-init to generate a new proxy cert or specify an alternate certifate in the configuration file."
                print "(either ~/.repoman-client)"
                sys.exit(1)
            if not (os.path.exists(self.usercert) or os.path.exists(self.userkey)):
                print "Your certificate and/or key doesn't exist as specified in"
                print "the config file."
                print "(either ~/.repoman-client)"
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
                       
    def return_usercert(self):
        return self.usercert
        
    def return_userkey(self):
        return self.userkey
        
    def return_repo(self):
        return self.repository
        
    def return_snapshot_location(self):
        return self.imagepath
        
    def return_snapshot_mount(self):
        return self.mountpoint
    
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
        user = self.rut.get_my_id(self.repository, self.usercert, self.userkey)
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
       
    def return_username(self):
        return self.rut.get_username(self.repository, self.usercert, self.userkey)
 
    def get_username(self):
        print self.rut.get_username(self.repository, self.usercert, self.userkey)
 
    def list_users(self, *args):
        if args[0]:
            #list long
            users = self.rut.get_users(self.repository, self.usercert, self.userkey, args[0])
            
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
        else:
            users = self.rut.get_users(self.repository, self.usercert, self.userkey, args[0])
            
            print "Users:"
            for user in users:
                print user.split('/')[5]
                
    def describe_user(self, user):
    
        resp = self.rut.query_user(self.repository, self.usercert, self.userkey, user)
        if resp.status == 404:
            print "User not found."
        
        else:
            resp = json.loads(resp.read())
            print '\n'
            for key in resp:
                if key == 'images':
                    print "  "+key+":"
                    for image in resp['images']:
                        print "  "+image
                else:
                    print "  "+key+": \t",
                    print resp[key]
                        
            print '\n'
            
    def describe_group(self, group):
        resp = self.rut.query_group(self.repository, self.usercert, self.userkey, group)
        if resp.status == 404:
            print "Group not found."
        
        else:
            resp = json.loads(resp.read())
            print '\n'
            for key in resp:
                print "  "+key+": \t",
                print resp[key]
            print '\n'
            
        
    def create_user(self, metadata):
        resp = self.rut.create_user(self.repository, self.usercert, self.userkey, metadata)
        if resp.status == 200:
            print 'User '+metadata['user_name']+' created.'
        elif resp.status == 409:
            print 'Username or client_dn conflict.  Maybe this user was already created?'
        elif resp.status == 400:
            print 'Invalid or insufficient parameters. Minimum parameters are: user_name, email, full_name, cert_dn. '
        else:
            print 'Unknown HTTP response code '+str(resp.status)
            
    def create_group(self, metadata):
        resp = self.rut.create_group(self.repository, self.usercert, self.userkey, metadata)
        if resp.status == 200:
            print 'Group '+metadata['name']+' created.'
        elif resp.status == 409:
            print 'Name conflict.  Maybe this group was already created?'
        elif resp.status == 400:
            print 'Invalid or insufficient parameters.  Minimum parameters: name.'
        else:
            print 'Unknown HTTP response code '+str(resp.status)
            
    def remove_user(self, user):
        resp = self.rut.remove_user(self.repository, self.usercert, self.userkey, user)
        if resp.status == 200:
            print 'User '+user+' has been removed..'
        elif resp.status == 404:
            print 'User '+user+' not found.'
        else:
            print 'Unknown HTTP response code '+str(resp.status)
            
    def remove_group(self, group):
        resp = self.rut.remove_group(self.repository, self.usercert, self.userkey, group)
        if resp.status == 200:
            print 'Group '+group+' has been removed.'
        elif resp.status == 404:
            print 'Group '+group+' not found.'
        else:
            print 'Unknown HTTP response code '+str(resp.status)
            
    def remove_image(self, image, **kwargs):
        resp = self.rut.remove_image(self.repository, self.usercert, self.userkey, image)
        if resp.status == 200:
            print 'Image '+image+' has been removed.'
        elif resp.status == 404:
            print 'Image '+image+' not found.'
        else:
            print 'Unknown HTTP response code '+str(resp.status)
        
    def modify_user(self, user, metadata):
        resp = self.rut.modify_user(self.repository, self.usercert, self.userkey, user, metadata)
        if resp.status == 200:
            print 'User '+user+' has been modified.'
        elif resp.status == 404:
            print 'User '+image+' not found.'
        else:
            print 'Unknown HTTP response code '+str(resp.status)
            
    def modify_group(self, group, metadata):
        resp = self.rut.modify_group(self.repository, self.usercert, self.userkey, group, metadata)
        if resp.status == 200:
            print 'Group '+group+' has been modified.'
        elif resp.status == 404:
            print 'Group '+group+' not found.'
        else:
            print 'Unknown HTTP response code '+str(resp.status)
    
    def list_user_images(self, user, *args):
        resp = self.rut.get_user_images(self.repository, self.usercert, self.userkey, user)
        if resp.status == 404:
            print "User does not exist."
            sys.exit(1)
        images = json.loads(resp.read())
        if args[0]:
            print "Images for user "+user+":"
            for image in images:
                print image
        else:
            print "Images for user "+user+":"
            for image in images:
                print image.split('/')[6]
    
    def list_images_sharedwith(self, long):
        resp = self.rut.get_user_images_sharedwith(self.repository, self.usercert, self.userkey)
        if resp.status == 404:
            print "User not found."
            sys.exit(1)
        images = json.loads(resp.read())
        if long:
            print "Images shared with "+self.rut.get_username(self.repository, self.usercert, self.userkey)+":"
            for image in images:
                print image
            sys.exit(0)
        else:
            print "Images shared with "+self.rut.get_username(self.repository, self.usercert, self.userkey)+":"
            sys.exit(0)
            
    def list_images_sharedwith_user(self, user, long):
        resp = self.rut.get_user_images_sharedwith_user(self.repository, self.usercert, self.userkey, user)
        if resp.status == 404:
            print "User "+user+" not found."
            sys.exit(1)
        images = json.loads(resp.read())
        if long:
            print "Images shared with "+user+":"
            for image in images:
                print image
            sys.exit(0)
        else:
            print "Images shared with "+user+":"
            for image in images:
                print image.split('/')[6]
            sys.exit(0)
            
    def list_images_sharedwith_group(self, group, long):
        resp = self.rut.get_user_images_sharedwith_group(self.repository, self.usercert, self.userkey, group)
        if resp.status == 404:
            print "User "+user+" not found."
            sys.exit(1)
        images = json.loads(resp.read())
        if long:
            print "Images shared with "+group+":"
            for image in images:
                print image
            sys.exit(0)
        else:
            print "Images shared with "+group+":"
            for image in images:
                print image.split('/')[6]
            sys.exit(0)
    
    
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
                
    def list_group_members(self, group, long):
        members = self.rut.list_group_members(self.repository, self.usercert, self.userkey, group)
        if members.status == 404:
            print "Group not found."
            sys.exit(1)
        if long:
            print str(members.read())
        else:
            print str(members.read())
            
            
            
    def list_groups(self, *args):
        resp = self.rut.list_groups(self.repository, self.usercert, self.userkey)
        if not resp.status == 200:
            print "An error occurred."
            sys.exit(1)
        if args[0]:
            groups = json.loads(resp.read())
            for group in groups:
                self.describe_group(group.split('/')[5])
                
        else:
            groups = json.loads(resp.read())
            print "Groups:"
            for group in groups:
                print group.split('/')[5]
                
                
    def list_users_groups(self, user, long):
        resp = self.rut.query_user(self.repository, self.usercert, self.userkey, user)
        if resp.status == 404:
            print "User not found."
            sys.exit(1)
        if long:
            groups = json.loads(resp.read())['groups']
            for group in groups:
                self.describe_group(group.split('/')[5])
        else:
            groups = json.loads(resp.read())['groups']
            print "Groups:"
            for group in groups:
                print group.split('/')[5]
        sys.exit(0)
            


    def list_images_raw(self):
        images = self.rut.get_images(self.repository, self.usercert, self.userkey)
        return images[1]

    def update_metadata(self, *args, **kwargs):
        metadata = kwargs['metadata']
        resp = self.rut.post_image_metadata('/api/images', self.repository, self.usercert, self.userkey, metadata=metadata)
        if kwargs['exists']:
            print "Updating metadata."
            
            resp = self.rut.update_image_metadata('/api/images', self.repository, self.usercert, self.userkey, image_name=metadata['name'], metadata=metadata)
            if resp.status == 200:
                print "Metadata modification complete."
                
            else:
                print "Metadata was not modified: "+str(resp.status)+" error returned by the server."
        else:
            if resp.status == 201:
                print "Metadata uploaded, image created."
            elif resp.status == 409:
                print "This image already exists.  Please modify it with modify-image or choose a new name."
                sys.exit(1)
            else:
                print "Image was not created: response code "+str(resp.status)
            


    def describe_image(self, image, *args, **kwargs):
        resp = self.rut.get_image_metadata(self.repository, self.usercert, self.userkey, image)
        if resp.status == 404:
            print '\n'
            print "This image does not exist."
            print '\n'
            sys.exit(1)
        else:
            resp = json.loads(resp.read())
            print '\n'
            for key in resp:
                print key+": \t",
                print resp[key]
            print '\n'
        sys.exit(0)
            
    
    def delete(self, name):
        resp = self.rut.delete_image(self.repository, self.usercert, self.userkey, name)
        if not str(resp):
            print "Image "+name+" deleted."



    def upload_snapshot(self, *args, **kwargs):
        metadata = kwargs['metadata']
        
        
        if not kwargs['snapshot_complete']:
            self.snapshot_system()
             
        print '''

        Uploading to the image repository. This can also take 
        time, depending on the speed of your connection
        and the size of your image...
        '''
        self.rut.post_image(self.repository,self.usercert,self.userkey, self.imagepath,metadata['name'])
        
        print '\n   Image successfully uploaded to  the repository at:\n    '
        print self.repository
        
        
    def snapshot_system(self):
        print '''
        Creating an image of the local filesystem.  
        This can take up to 10 minutes or more.
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
            print "Syncing image."
            self.iut.sync_filesystem(self.mountpoint, self.excl_dirs)
            
        print "Snapshot process complete."

            
    

    def upload_image(self, file, *args, **kwargs):
        print "Uploading image "+file+" with name "+kwargs['image']
        self.rut.post_image(self.repository,self.usercert,self.userkey,file,kwargs['image'])
         
        
     
    def list_all_images(self):
        image_list = self.rut.get_all_images(self.repository, self.usercert, self.userkey)
        print "All images:"
        for item in image_list:
            print item.split('/')[6]
        
          
    def post_image(self,imagename):  
        self.rut.post_image(self.repository,self.usercert,self.userkey, self.imagepath,imagename)


    def share_user(self, image, user):
        resp = self.rut.share_user(self.repository, self.usercert, self.userkey, image, user) 
        if resp.status == 200:
            print "Share complete."
        elif resp.status == 404:
            print "Image not found."
        elif resp.status == 400 or resp.status == 403:
            print "User not found."
        else:
            print "Share failed: HTTP code "+str(resp.status)

    def share_group(self, image, group):
        resp = self.rut.share_group(self.repository, self.usercert, self.userkey, image, group) 
        if resp.status == 200:
            print "Share complete."
        elif resp.status == 404:
            print "Image not found."
        elif resp.status == 400 or resp.status == 403:
            print "Group not found."
        else:
            print "Share failed: HTTP code "+str(resp.status)

    def unshare_user(self, image, user):
        resp = self.rut.unshare_user(self.repository, self.usercert, self.userkey, image, user) 
        if resp.status == 200:
            print "Unshare complete."
        elif resp.status == 404:
            print "Image not found."
        elif resp.status == 400 or resp.status == 403:
            print "User not found."
        else:
            print "Unshare failed: HTTP code "+str(resp.status)

    def unshare_group(self, image, group):
        resp = self.rut.unshare_group(self.repository, self.usercert, self.userkey, image, group) 
        if resp.status == 200:
            print "Unshare complete."
        elif resp.status == 404:
            print "Image not found."
        elif resp.status == 400 or resp.status == 403:
            print "Group not found."
        else:
            print "Share failed: HTTP code "+str(resp.status)
            
    def add_users_to_group(self, group, users):
        for user in users:
            resp = self.rut.add_user_to_group(self.repository, self.usercert, self.userkey, group, user)
            if not resp.status == 200:
                if resp.status == 404:
                    print "User or group not found."
                else:
                    print "HTTP error "+resp.status
                sys.exit(1)
        print "Users successfully added to group "+group+"."
        
    def remove_users_from_group(self, group, users):
        for user in users:
            resp = self.rut.remove_user_from_group(self.repository, self.usercert, self.userkey, group, user)
            if not resp.status == 200:
                if resp.status == 404:
                    print "User or group not found."
                else:
                    print "HTTP error "+resp.status
                sys.exit(1)
        print "Users successfully removed from group "+group+"."
        
    def add_permissions(self, group, permissions):
        for permission in permissions:
            resp = self.rut.add_permission(self.repository, self.usercert, self.userkey, group, permission)
            if not resp.status == 200:
                if resp.status == 404 or resp.status == 400:
                    print "Group or permission not found."
                else:
                    print "HTTP error "+resp.status
                sys.exit(1)
        print "Permissions succesfully added to group "+group+"."
        
    def remove_permissions(self, group, permissions):
        for permission in permissions:
            resp = self.rut.remove_permission(self.repository, self.usercert, self.userkey, group, permission)
            if not resp.status == 200:
                if resp.status == 404 or resp.status == 400:
                    print "Group or permission not found."
                else:
                    print "HTTP error "+resp.status
                sys.exit(1)
        print "Permissions succesfully removed from group "+group+"."


    
    def get(self, image, dest):
        resp = self.rut.get_image_metadata(self.repository, self.usercert, self.userkey, image)
        if not resp.status == 200:
            if resp.status == 404:
                print "Image "+image+" does not exist."
                sys.exit(1)
            else:
                print "Unknown error "+resp.status
                sys.exit(1)
        print "Downloading image "+image+" and storing it at "+dest+"."
        resp = json.loads(resp.read())
        if resp['raw_file_uploaded']:
            self.rut.download_image(self.repository,self.usercert,self.userkey,image,dest)
        else:
            print "The raw image for "+image+" has not been uploaded yet."
            sys.exit(0)
        print "Image downloaded successfully."

