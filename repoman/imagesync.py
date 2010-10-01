#!/usr/bin/env python
'''
Created on Sep 17, 2010

@author: fransham
'''
import getopt
import pwd
import sys
import os
from socket import *
import getpass
import subprocess
from commands import getstatusoutput

repo = "alto.cloud.nrc.ca"
    
def usage():
    print "coming soon stay tuned"
    
    
def connect():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((repo,21567))
    return sock

def list_images(username):
    sock = connect()
    sock.send("list "+username)
    print ""
    print "Repository:" + repo
    print ""
    while 1:
        data = sock.recv(1024)
        if not data:
            sock.close()
            sys.exit(0)
        print data
        print " "
        print " "
    print ""
    sock.close()
        
def get_url(imagename, username):
        sock = connect()
        sock.send("geturl "+imagename+" "+username)
        print ""
        print sock.recv(1024)
        print ""
        sock.close()

def save_image(imagename, username):
    sock = connect()
    sock.send("geturl "+imagename+" "+username)
    url = sock.recv(1024)
    sock.close()
    
    print url
    #check if this image already exists
    if url.startswith("http"):
        print "\n This operation will overwrite the image named:"
        print " "+imagename
        print " available at: " 
        print url
        print ""
        if not ask_yes_or_no():
            sys.exit(0)
        
    else:
        print "you are creating a new image named "+imagename
        
        
    if os.path.exists("/var/lock/interactive.sh.lock"):
        print "rsync already in progress..."
        f=open("/var/lock/interactive.sh.lock")
        rsyncpid = f.read()
        os.waitpid(rsyncpid)
    else:
        already_mounted = False;
        for line in open("/etc/mtab"):
            if "/mnt/filesystemcopy.img /mnt/fscopy" in line:
                already_mounted = True;
                break
        if not already_mounted:
            print "creating new image of the filesystem... please wait."
            ret,output = getstatusoutput("sudo ./interactive.sh")
            if ret:
                print output
                sys.exit(1)
        else:
            print "syncing filesystem to the existing image"
            ret,output = getstatusoutput("sudo rsync -ax --exclude /dev --exclude /proc --exclude /sys --exclude /mnt --exclude /tmp / /mnt/fscopy")
            if ret:
                print output
                exit (1)
            
   
    
    sock = connect()
    sock.send("save "+imagename+" "+username)
    mountpoint = sock.recv(1024)
    
    if not mountpoint.startswith("/tmp/"):
        print "ERROR: "+ mountpoint
        sys.exit(2)
    
    
    mycmd = "/usr/bin/sudo /usr/bin/rsync --delete -avx --exclude /dev --exclude /proc --exclude /sys / "+username+"@"+repo+":"+mountpoint
    #spawn a subprocess to do the rsync:
    print mycmd
    output = subprocess.Popen(mycmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print "copying...",
    while output.poll()==None:
        print ".",
        sock.send("copying")
        if not sock.recv(1024).startswith("okay"):
            print "Something went awry...  killing the rsync process now."
            #flag the image as bad in the DB
            output.kill()
            break
    
    if output.returncode():
        print "rsync finished with errors:" 
        print output.communicate[1]
        print ""
        print "Please address and try your copy again"
        sock.send("error")
        sock.close()
        sys.exit(1)
    
    sock.send("complete")
    print sock.recv(1024)
    sock.close()
    
    print "\n Image "+imagename+" successfully save in repository."
    
    
    
    

def ask_yes_or_no():
    print " Are you sure you want to continue?"
    k=raw_input("[y/N]")
    if k in ('y', 'ye', 'yes'): 
        return True
    return False

def main(argv):              
    try:                                
        opts, args = getopt.getopt(argv, "hd", 
                                   ["help", 
                                    "debug",
                                    "list",
                                    "geturl",
                                    "save",
                                    "name=",
                                    "user=",
                                    "repo="
                                    ]) 
        
    except getopt.GetoptError:           
        usage()                          
        sys.exit(2)  
                           
    list = False
    geturl = False
    save = False
    username = pwd.getpwuid(os.getuid()).pw_name
    name = ""
    newname = ""
    
    for opt, arg in opts:                
        if opt in ("-h", "--help"):      
            usage()                     
            sys.exit()                  
        elif opt == ("-d", "--debug"):                
            global _debug               
            _debug = 1                  
        elif opt in ("--list"): 
            list = True
        elif opt in ("--geturl"):
            geturl = True
        elif opt in ("--save"):
            save = True
        elif opt in ("--name"):
            name = arg
        elif opt in ("--user"):
            username = arg
        elif opt in ("--repo"):
            repo = arg
    
    #make sure only one command line argument is specified:         
    if( list + geturl + save != 1):
        usage()
        sys.exit(2) 
      

    if list:
        list_images(username)
        sys.exit(0)
        
    if geturl:
        if not name:
            print "\n please specify an image name with the --name flag. \n"
            sys.exit(2)
        get_url(name,username)
            
    if save:
        if not name:
            print "\n please specify an image name with the --name flag. \n"
            print "the images available to you are :"
            list_images(username)
            print "select one of these images to overwrite, or specify a new image name"
            print "see --help for more details"
            sys.exit(2)
        save_image(name, username)
          
        
        
if __name__ == "__main__":
    main(sys.argv[1:])