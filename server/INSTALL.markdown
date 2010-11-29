# REPOMAN

There are 2 ways to install repoman.

1.  From an Egg

    This is the recomended way to install and run repoman

1.  From a checked out repository

    This method will allow you to develop and test repoman


## Install from an Egg (recommended)
1.  Install prerequisites
        yum install python-setuptools gcc sqlite sqlite-devel
        easy_install pip virtualenv

1.  Create a Virtual Environment
        virtualenv --no-site-packages /opt/repoman

1.  Activate the virtual env
        cd /opt/repoman
        source bin/activate

1.  Install repoman
        pip install repoman

1.  Create a file for populating the database with administrators
        vim  $HOME/repoman_admins

    The file should contain lines containing `username,email,client_dn', with no trailing space or lines.

    Example file:
        bob,bob@uvic.ca,/C=CA/O=Grid/OU=phys.uvic.ca/CN=Bob McKenzie
        doug,doug@uvic.ca,/C=CA/O=Grid/OU=phys.uvic.ca/CN=Doug McKenzie

1.  Create and edit the application config
        paster make-config repoman deploy.ini

    Make sure to point `admin_file` to the file you created in the previous step

1.  Create the database
        paster setup-app deploy.ini

    If using the default sqlite DB, ensure that the `apache` user has read/write
    permissions on the database file and the base directory the database file is in.

1.  Create the apache configs
        paster --plugin=repoman make-wsgi-config deploy.ini

1.  Modify the `repoman.conf`

    Make `SSLCertificateFile` point to your host certificate

    Make `SSLCertificateKeyFile` point to your host certificate key

    Make `SSLCACertificatePath` point the directory that contains your Root CA certificates for verifying clients

    Make `SSLCARevocationPath` point to the directory that contains your CRLs for the Root CA certificates

1.  Copy `repoman.conf` to your apache config directory
        cp repoman.conf /etc/httpd/conf.d

1.  Start Apache
        sudo service httpd restart

## Run directly from a checked out repository
**`$REPOMAN` is used throughout this section to indicate the path to the virtualenv created in step one**

**Assume that once the virtualenv has been activated it remains active**

**This guide assumes a RHEL based OS.  paths and commands may vary for you**

1.  Install prerequisites

        yum install python-setuptools gcc sqlite sqlite-devel
        easy_install pip virtualenv

1.  Create a Virtual Environment
        mkdir -p /opt/repoman
        export REPOMAN=/opt/repoman
        virtualenv --no-site-packages $REPOMAN

1.  Install needed libraries
        cd $REPOMAN
        source bin/activate
        pip install pylons sqlalchemy simplejson

1.  If running Python 2.4 install extra libraries
        pip install pysqlite uuid

1.  Checkout the repository
        git clone git://github.com/hep-gc/repoman.git

    or if you don't have git installed:
        wget --no-check-certificate https://github.com/hep-gc/repoman/tarball/dev
        tar xzvf hep-gc-repoman*.tar.gz
        rm -Rf hep-gc-repoman*.tar.gz
        mv hep-gc-repoman* repoman

1.  Modify repoman.wsgi
        cd $REPOMAN/repoman/server/apache
        vim repoman.wsgi

    Replace `@@VIRTUAL_ENV@@` with `$REPOMAN`.

    or
        sed -i "s|@@VIRTUAL_ENV@@|$VIRTUAL_ENV|" repoman.wsgi


1.  Copy the  config to your apache installation.
        cp $REPOMAN/repoman/server/apache/repoman.conf /etc/httpd/conf.d/
        vim /etc/httpd/conf.d/repoman.conf

    Replace `@@VIRTUAL_ENV@@` with `$REPOMAN`.

    or

        sed -i "s|@@VIRTUAL_ENV@@|$VIRTUAL_ENV|" /etc/httpd/conf.d/repoman.conf

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
        cd $REPOMAN/repoman/server/repoman/
        paster setup-app development.ini

1. Give the `apache` user read/write on the database
        cd $REPOMAN/repoman/server
        sudo chown apache:apache repoman
        sudo chown apache:apache repoman/development.db

1. Start Apache
        sudo /etc/init.d/httpd start

