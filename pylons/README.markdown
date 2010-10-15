# REPOMAN

## Development Environment

Install everything in a virtual environment:
    virtualenv --no-site-packages repoman
    cd repoman
    source bin/activate
    easy_install pylons sqlalchemy

If using python 2.4:
    easy_install pysqlite uuid

Checkout the project into the virtual environment:
    git clone git@github.com:hep-gc/repoman.git
    git checkout dev

Modify the wsgi application at *pylons/repository/apache/repo_app.wsgi*
It should look like this:
    import site
    site.addsitedir('{FULLPATH_TO_TE_VIRTUALENV}/lib/python2.4/site-packages')

    import os, sys
    sys.path.append('{FULLPATH_TO_TE_VIRTUALENV/repoman/pylons/repository}')
    os.environ['PYTHON_EGG_CACHE'] = '{FULLPATH_TO_TE_VIRTUALENV}/python-eggs'

    from paste.deploy import loadapp
    application = loadapp('config:{FULLPATH_TO_TE_VIRTUALENV}/repoman/pylons/repository/development.ini')

Create the cache directory for eggs
    mkdir python-eggs

Create a file *$HOME/repoman_admins* to initially populate the database with users:
Each line of the file should be of the form *name,email,dn*.  No trailing space or empty lines!

Example:
    Fake Name,fn@domain.ca,/C=CA/O=Grid/OU=domain.ca/CN=Fake Name

Create the database:
    paster setup-app developmen.ini
    # you should see the sql statements that created the db echoed to your screen
    chown apache:apache devlopment.db

Copy the example *repoman.conf* virtualhost file to your Apache config and modify

If not already installed, install mod_ssl and mod_wsgi.  
A mod_wsgi compiled against Python2.4 is available in the EPEL repository.
If using a version of python, you must build from source

Start httpd!



## Production Environment

application will be an installable python egg.
Stay tooned!