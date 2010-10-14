# Repoman

## What Is It?
Repoman is the beginnings of a virtual machine image management system accessed
via a RESTful API.  HTTP error codes and non-standard headers (*they will be documented though!*)
will be heavily used throughout the API to provide meaningful error states to the user.

## Basic Objects
Currently there are three basic objects accessible by users.  These
are `user`, `group`, and `image`.

Note see `REST.markdown` for a rough specification of what information is accessible.

### Users
* Each `user` object defines a user of the system, including system admins.
* Typical information such as names, email, distinguished_name, etc. are accessible
from the `user` object.
* References to `image` and `group` objects will also be
available.

### Groups
* Each `group` object contains a list of users that are members of the specified group.
* Within each group there will be the concept of regular users as well as group-admins.

### Images
* Images are referenced by UUID
* Each `image` object describes a single image uploaded by a user.
* Each `image` is owned by a specific user, and is a member of a group.
* File permissions on the image can be specified to allow for sharing the image
among group members.  Sharing is optional however.


## User Authentication
User access to Repoman is regulated by the usage of x509 certificates, there is
no concept of usernames and passwords to gain access.  The validation of client
certificates is done by mod_ssl, while authentication of the user is done by
looking up the clients' distinguished name within the Repoman database.  If the
client certificate checks out and the user is in the database, they will have
access to the API.  If either the certificate is invalid or the user is not found
in the database, they will be denied access to the API.


## User Actions
A user will be able to:

* View a list of all users
* View a list of all groups
* View a list of their groups
* View a list of all group members
* View a list of images owned by them
* View a list of images shared within a group
* View detailed information of images owned or shared with them
* Create and upload a new image
* Modify image information
* Overwrite an image with a newer image
* Copy an existing image (owned or shared) to a new image
* other stuff?

## Group Admin Actions
* add an existing user to group
* modify/create/delete any image associated group

## Admin Actions
* Basically *root* user
* Add/delete users
* Create/delete groups
* modify group permissions
* etc.

## Technology
Repoman is built on the following software:

* Apache HTTP webserver
  * Provides the webserver, and easy access to openssl, etc.
  * Who doesn't like Apache?
* mod_ssl
  * Provides ssl and client cert authentication
  * Proxy-certs can be used if an appropriate version of openssl is used
* mod_wsgi
  * Provides integration between Python and Apache
  * Enables direct access to Apache environment variables by the python app

* Pylons
  * One of the **big** two Python web-app frameworks
  * WSGI compliant
  * SQLAlchemy Support (this is very nice to have)
  * Templating engine for future graphical interface
  * **easy** rest controllers (built-in)
  * **easy** xmlrpc controllers (built-in)
  * very flexible.  If you don't like something, change it or replace it

* Python Modules:
  * simplejson - as the name implies, very simple json encode/decode
  * uuid - uuid generation.  (standard in Python 2.5+)
  * sqlalchemy - ORM with support for most common databases

