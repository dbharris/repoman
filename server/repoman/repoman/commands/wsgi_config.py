from paste.script.command import Command
import os
import sys

wsgi_template = """
#-*- VIRTUAL_ENV -*-

#-*- CONFIG -*-


import site
site.addsitedir('%s/lib/python2.4/site-packages' % VIRTUAL_ENV)

import os, sys
os.environ['PYTHON_EGG_CACHE'] = '%s/python-eggs' % VIRTUAL_ENV

from paste.deploy import loadapp
application = loadapp('config:%s' % CONFIG)

"""

apache_template = """

<VirtualHost localhost:443>

    ServerName localhost

    # Enable SSL and disable SSLv2
    SSLEngine on
    SSLProtocol all -SSLv2

    # Your host certificate/key
    SSLCertificateFile /opt/repo/certs/server.crt
    SSLCertificateKeyFile /opt/repo/certs/server.key

    # Trusted certs use to authenticate clients
    SSLCACertificatePath /opt/repo/certs/ca
    SSLCARevocationPath /opt/repo/certs/ca_revoke

    # Needed to pass ssl variables to the application
    SSLOptions +StdEnvVars

    # Verify client certs
    SSLVerifyClient optional
    SSLVerifyDepth 10
    # Verify host to host communications
    SSLProxyVerify require
    SSLProxyVerifyDepth 10

    #-*- WSGIScriptAlias1 -*-


</VirtualHost>

##
## Uncomment the Below virtualhost if you want to allow http access to repoman.
##
## By enabling http access, you will NOT be comprimizing your repoman install!
## It simple enables images(on a per image basis) to be downloaded via http.
#<VirtualHost localhost:80>
#
#    ServerName localhost
#
#    -*- WSGIScriptAlias2 -*-
#
#
#</VirtualHost>

"""

class WSGIConfigCommand(Command):
    #TODO: clean this up!!!

    min_args = 1
    max_args = 1

    summary = "Run this from the root directory of your virtual environment"
    usage = ""
    group_name = "repoman"
    parser = Command.standard_parser(verbose=False)

    wsgi_template = wsgi_template
    apache_template = apache_template
    wsgi_alias = 'WSGIScriptAlias / %s\n'

    def command(self):
        base_dir = os.path.realpath('.')
        print "Creating 'repoman.wsgi'"
        wsgi_config = open('repoman.wsgi', 'w')
        wsgi_config.write(self.wsgi_template)
        wsgi_config.close()
        print "Customizing 'repoman.wsgi' with:"
        print "\tVIRTUAL_ENV\t<-- %s" % base_dir
        print "\tCONFIG\t\t<-- %s" % base_dir + '/' + self.args[0]
        self.insert_into_file('repoman.wsgi', 'VIRTUAL_ENV', "VIRTUAL_ENV = '%s'\n" % base_dir)
        self.insert_into_file('repoman.wsgi', 'CONFIG', "CONFIG = '%s'\n" %(base_dir+'/'+self.args[0]))

        print "Creating apache config `repoman.conf`"
        apache_config = open('repoman.conf', 'w')
        apache_config.write(self.apache_template)
        apache_config.close()
        print "Customizing 'repoman.wsgi' with:"
        print "\t WSGIScriptAlias\t<-- %s" % (self.wsgi_alias % (base_dir+'/'+'repoman.wsgi'))
        self.insert_into_file('repoman.conf', 'WSGIScriptAlias1',
                               self.wsgi_alias % (base_dir+'/'+'repoman.wsgi'),
                               indent=True)
        self.insert_into_file('repoman.conf', 'WSGIScriptAlias2',
                               '#    ' + self.wsgi_alias % (base_dir+'/'+'repoman.wsgi'),
                               indent=True)

        print 'Configuration Completed.'
        print ''
        print 'Next Steps:'
        print '    1. Modify repoman.conf to set your ssl certificates and hostname.'
        print '    2. Copy repoman.conf to your apache config directory'

