def make_config(repository, snapshot_image, snapshot_mount, custom_cert, **kwargs):
    if custom_cert:
        usercert = 'usercert: '+kwargs['usercert']
        userkey = 'userkey: '+kwargs['userkey']
    else:
        usercert = '#usercert: /tmp/x509up_u[USER_ID]'
        userkey = '#userkey: /tmp/x509up_u[USER_ID]'
        
    return """
#Repoman-client 0.2 Configuration File

[ThisImage]

#Enter your Repoman repository address in the form https://HOST:POST
repository: %s

#Repoman-client will look in /tmp/x509up_u[USER_ID] by default.
#If you'd like to specify an alternate cert to use, uncomment the next two lines and change the location.
%s
%s


# Directories to exclude from syncing (for snapshot). 
# If these are not set, the sync could take much longer.
exclude_dirs: /dev /mnt /lustre /proc /sys /tmp /etc/grid-security /root/.ssh


#Location to store the snapshot image for upload:
image: %s

#Location to mount the snapshot image for filesystem sync:
mountpoint: %s

# Do you want to create an initial copy of the filesystem on boot?
# Default is true, as this speeds things up a lot.  Uncomment to
# skip.
# sync_onboot: false


# Lock file for allowing only one rsync process at a time.
# Default is fine, but change this if you want...
# lockfile: /var/lock/reposync.pid
    """ %(repository, usercert, userkey, snapshot_image, snapshot_mount)
