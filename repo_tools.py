'''
Created on Sep 16, 2010

@author: fransham
'''

import MySQLdb
import re
import os
from commands import getstatusoutput



class ImageRepository(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.fdisk_path="/sbin/fdisk"
        self.uuidgen_path="/usr/bin/uuidgen"
        self.fuse_mountlo_path="/opt/bin/mountlo"
        self.fusermount_path="/bin/fusermount"
        
    def connect(self):
        self.conn = MySQLdb.connect (read_default_file="~/.my.cnf")
        self.cursor = self.conn.cursor()
    
    def disconnect(self):
        self.cursor.close()
        self.conn.close()
    
    def query_db(self, query):
        self.connect()
        self.cursor.execute(query)
        row = self.cursor.fetchall()
        self.disconnect()
        return row
        
    def get_images(self, username):
        result = self.query_db( "SELECT name,url FROM image WHERE owner = '" + username + "'")
        for i in result:
            print i
        return result
    
    def image_exists(self, image_name, username):
        result = self.query_db( "SELECT name FROM image WHERE name = '" + image_name + 
                             "' AND owner = '" + username + "'")
        if result:
            return True
        return False
    
    def get_url(self, image_name, username):
        if not self.image_exists(image_name, username):
            return (("that user or image doesn't exist",),)
            
        result = self.query_db("SELECT url FROM image WHERE name = '" + image_name + 
                             "' AND owner = '" + username + "'")
        return result
    
    def mount(self, image_name, username):
        if not self.image_exists(image_name, username):
            raise MountError("mount", " That image doesn't exist")
        
        #get the path to the image
        result = self.query_db("SELECT path FROM image WHERE name = '" + image_name + 
                             "' AND owner = '" + username + "'")
        imagepath = result[0][0]
        print imagepath
        
        #create directory in /tmp
        ret, output = getstatusoutput(self.uuidgen_path)
        if ret:
            raise MountError("uuidgen", "could not generate a uuid: "+output)    
        mountdir = "/tmp/" + output + "/"     
        
        #create the mount directory:
        os.mkdir(mountdir)
        
        #get the offset of the partition:
        offset = self._guess_offset(imagepath)
        
        #mount the image:
        ret, output = getstatusoutput("sudo /sbin/losetup -fv -o "+str(offset) + " "+imagepath)
        if ret:
            raise MountError("/sbin/losetup", "losetup failed: "+output)  

        loop_device = output.rsplit()[3]
        if not loop_device.startswith("/dev/loop"):
            raise MountError("/sbin/losetup", "losetup failed: "+output)  
        
        ret, output = getstatusoutput(self.fuse_mountlo_path+" "+loop_device+" "+mountdir)
        if ret:
            raise MountError("fuse_ext2", "Fuse Mounting Failed: "+output) 
 
         
        #add mounted_at to db
        self.query_db("UPDATE image set mounted_at='" + mountdir + 
                      "' WHERE name = '" + image_name + "' AND owner = '" + username + "'")
        self.query_db("UPDATE image set  loop_device='"+loop_device+ 
                      "' WHERE name = '" + image_name + "' AND owner = '" + username + "'")
        #add error_checking
        return mountdir
    
    def umount(self, image_name, username):
        result = self.query_db("SELECT mounted_at,loop_device FROM image WHERE name = '" + image_name + 
                             "' AND owner = '" + username + "'")
        loop_device=result[0][1]
        mountdir = result[0][0]
        if not result or mountdir.startswith("None"):
            raise MountError("umount","that image doesn't exist or is not" +
                             " currently mounted")
        
        #add mounted_at to db
        self.query_db("UPDATE image set mounted_at=NULL"+ 
                      " WHERE name = '" + image_name + "' AND owner = '" + username + "'")
        self.query_db("UPDATE image set loop_device=NULL"+ 
                      " WHERE name = '" + image_name + "' AND owner = '" + username + "'")
        
        ret, output = getstatusoutput(self.fusermount_path+" -u " + mountdir)        
        os.rmdir(mountdir)
        
        if ret:
            raise MountError("fusermount -t", "unmounting failed: "+output)
        
        ret, output = getstatusoutput("/sbin/losetup -d " + loop_device)
        if ret:
            raise MountError("fusermount -t", "unmounting failed: "+output) 
            
        return True
    
    def copy(self,image_name, new_name, username):
        if not self.image_exists(image_name, username):
            print "that image doesn't exist"
            return False
        #insert copy magic here
        return True;
    
    def delete(self, image_name, username):
        if not self.image_exists(image_name, username):
            print "that image doesn't exist"
            return False
        #insert delete magic here
        return True;
        
    def create_db(self):
        #implement this later
        return True
    
    def flag_as_bad(self, image_name, username):
        #something went wrong with the copying...  don't use this image
        print "badness!"
        
    def _guess_offset(self, imagepath):
        # this code taken from the nimbus project's way of mounting images.
        cmd = "%s -lu %s" % (self.fdisk_path, imagepath)

        ret,output = getstatusoutput(cmd)
        if ret:
            errmsg = "problem running command: '%s' ::: return code" % cmd
            errmsg += ": %d ::: output:\n%s" % (ret, output)
            raise MountError("fdisk:", errmsg)

        part_pattern = re.compile(r'\n%s.*' % imagepath)
        lines = []
        for m in part_pattern.finditer(output):
            lines.append(m.group())

        if len(lines) == 0:
            #offset is 0
            return 0
            #raise MountError("fdisk"," 1- stdout is not parseable: '%s'" % output)

        firstparts = lines[0].split()
        if len(firstparts) < 5:
            raise MountError("fdisk2"," 2- stdout is not parseable: '%s'" % output)

        if firstparts[1] == "*":
            sector_count = firstparts[2]
        else:
            sector_count = firstparts[1]

        try:
            sector_count = int(sector_count)
        except:            
            raise  MountError("fdisk3","3- stdout is not parseable, sector_count is not an integer ('%s'), full output: '%s'" % (sector_count, output))
            
        offset = 512 * sector_count
        
        return offset


        
class MountError(Exception):
    """Exception raised when the system cannot mount the specified file.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- system error from mount command
    """

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

        
