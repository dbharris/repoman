'''
Created on Oct 4, 2010

@author: fransham
'''

from os import makedirs,path,mkdir
from commands import getstatusoutput

class imageutils(object):
    '''
    classdocs
    '''
        
    def create_image(self,imagepath):
        
        dir = path.dirname(imagepath)
        if not path.exists(dir):
            makedirs(dir)
        ret1, fs_size = getstatusoutput("df /")
        ret2, fs_bytes_used = getstatusoutput("df /")
        ret3, image_dirsize = getstatusoutput("df "+dir)
        
        if(ret1 or ret2 or ret3):
            raise MountError("df ", "error getting filesystem sizes: \n"+ret1+ret2+ret3)
        
        fs_size=fs_size.split()[8]
        fs_bytes_used=fs_bytes_used.split()[9]
        image_dirsize = image_dirsize.split()[10]
        
        if(int(image_dirsize) < int(fs_bytes_used)):
            raise MountError("df ", "ERROR: Not enough space on filesystem. \n" +
                             "Check the path to your image ("+imagepath+") "+
                             "in /etc/repoman-client/repoman-client.conf and retry")
        if(int(image_dirsize) < int(fs_size)):
            print ("WARNING: the directory you have specified for your image copy"+
                   "is smaller in size than the root directory.  Your new image"+
                   "will have less free space.")
            fs_size = fs_bytes_used
        
        print "creating image "+imagepath    
        ret4, dd = getstatusoutput("dd if=/dev/zero of="+imagepath+" count=0 bs=1k seek="+str(fs_size))
        if ret4:
            raise MountError("dd", "ERROR: problem creating image "+imagepath+": "+dd)
        
        print "creating ext3 filesystem on "+imagepath
        ret5, mkfs = getstatusoutput("mkfs -t ext3 -F "+imagepath)
        if ret5:
            raise MountError("mkfs.ext3: ", "ERROR: problem with mkfs: "+mkfs)
        
            
        
    def mount_image(self,imagepath,mountpoint):
        if not path.exists(mountpoint):
            makedirs(mountpoint)
        print "mounting image "+imagepath+" on "+mountpoint
        ret, mnt = getstatusoutput("mount -o loop "+imagepath+" "+mountpoint)
        if ret:
            raise MountError("mount -o loop", "ERROR: Mounting of image failed: "+mnt)
        
    
    def check_mounted(self,imagepath, mountpoint):
        for line in open("/etc/mtab"):
            if imagepath in line:
                return True
        return False
                
    def sync_filesystem(self, mountpoint, excl_dirs):
        create_dirs = ['/dev','/mnt','/proc','/sys','/tmp']
        for i in create_dirs:
            if not path.exists(mountpoint+i):
                mkdir(mountpoint+i)
        excludes = str.rsplit(excl_dirs)
        cmd = "rsync -ax --delete"
        for excl in excludes:
            cmd += " --exclude "+excl
        cmd += " / "+mountpoint
        print "creating local copy of filesystem... this could take some time.  Please be patient."
        ret, sync = getstatusoutput(cmd)
        if ret:
            raise MountError("rsync ","ERROR: rsync returned errors: "+ sync)
        print "local copy of VM created."
        


    def __init__(self):
        '''
        Constructor
        '''
 

class MountError(Exception):
    """Exception raised when the system cannot mount the specified file.

Attributes:
expr -- input expression in which the error occurred
msg -- system error from mount command
"""

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

      
