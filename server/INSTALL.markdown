# REPOMAN

There are 2 ways to install repoman.

1.  From an Egg

1.  From a checked out repository

**`$REPOMAN` is used throughout this section to indicate the path to the virtualenv created in step one**

**Assume that once the virtualenv has been activated it remains active**

**This guide assumes a RHEL based OS.  paths and commands may vary for you**


## Install from an Egg



## Run directly from a checked out repository

1.  Create a Virtual Environment
        virtualenv --no-site-packages repoman

1.  Install needed libraries
        cd $REPOMAN
        source bin/activate
        pip install pylons sqlalchemy simplejson

1.  If running Python 2.4 install extra libraries
        pip install pysqlite uuid

1.  Checkout the repository
        git clone git@github.com:hep-gc/repoman.git

1.  Modify repoman.wsgi
        cd $REPOMAN/repoman/server
        vim repoman.wsgi

    Replace `@@VIRTUAL_ENV@@` with `$REPOMAN`.

1.  Copy the  config to your apache installation.
        cp $REPOMAN/repoman/server/apache/repoman.conf /etc/httpd/conf.d/
        vim /etc/httpd/conf.d/repoman.conf

    Replace `@@VIRTUAL_ENV@@` with `$REPOMAN`.
    Modify the paths to the host and CA certificates if needed.

1.  Create the cache directory for eggs
        mkdir $REPOMAN/python-eggs

1.  If not already installed on your system, install `mod_wsgi` and `mod_ssl`

    `mod_wsgi` is available from the EPEL repository.  At the time of writing, there are modules for python2.4 and python 2.6/

1.  In your home directory create a file for populating the database with administrators
        vim  $HOME/repoman_admins

    The file should contain lines containing `username,email,client_dn', with no trailing space or lines.

    Example file:
        bob,bob@uvic.ca,/C=CA/O=Grid/OU=phys.uvic.ca/CN=Bob McKenzie
        doug,doug@uvic.ca,/C=CA/O=Grid/OU=phys.uvic.ca/CN=Doug McKenzie

1. Create the database
        cd $REPOMAN/repoman/server
        paster setup-app development.ini

1. Give the `apache` user read/write on the database
        cd $REPOMAN/repoman/server
        sudo chown apache:apache repoman
        sudo chown apache:apache repoman/development.db

1. Start Apache
        sudo /etc/init.d/httpd start

