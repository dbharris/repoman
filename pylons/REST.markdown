# RESTfull API

## URLs

    <host:port>/repository/users
    <host:port>/repository/users/{id}
    <host:port>/repository/groups
    <host:port>/repository/groups/{id}
    <host:port>/repository/images
    <host:port>/repository/images/{id}

***
## repository/users
### GET
A GET request will return a list of all users in the system formatted as a json
list of objects.

each object will contain:
    uuid        - string - 32 character hex representation of the uuid
    name        - string - the users name
    email       - string - the users email
    client_dn   - string - the users DN from their grid cert
    admin       - bool   - is the user an admin?

### POST
POSTing to this url will insert a new entry into the database.

required params:
    name        - plain text name of the user
    email       - email address of the user
    client_dn   - client DN (must be unique among all users)

optional params:
    admin       - bool   - is the user an admin?
    suspended   - bool   - is the account suspended?
    groups      - string - a list of group uuids to add this user to


***
## repository/users/{id}
### GET
A GET request on this url will retrieve an object describing the specified user
in detail formatted in json.

each response will be a json object containing:
    uuid        - string - 32 character hex representation of the uuid
    name        - string - the users name
    email       - string - the users email
    client_dn   - string - the users DN from their grid cert
    admin       - bool   - is the user an admin?
    suspended   - bool   - is the account suspended?
    groups      - list   - a list of groups the user is a member of
    images      - list   - a list of images the user owns


***
## repository/groups
### GET
A GET request on this url will retrieve list of objects describing all groups
formatted in json.

each object will contain:
    uuid        - string - 32 character hex representation of the uuid
    name        - string - name of the group


### POST
POSTing to this url will insert a new entry into the database.

required params:
    name        - string - plain text name of the group

optional params:
    users       - string - comma seperated list of user uuids to add to the group

***
## repository/group/{id}
### GET
A GET request on this url will retrieve an object describing the specified group
in detail formatted in json.

each response will be a json object containing:
    uuid        - string - 32 character hex representation of the uuid
    name        - string - the users name
    users       - list   - a list of all users who are members of the group


***
## repository/images
### GET
A GET request on this url will retrieve list of objects describing all images
formatted in json.

each object will contain:
    uuid        - string - 32 character hex representation of the uuid
    name        - name of the image
    owner_uuid  - string - 32 character hex representation of the uuid
    group_uuid - string - 32 character hex representation of the uuid


### POST
POSTing to this url will insert a new entry into the database.

required params:
    name        - string - plain text name of the group
    file        - file   - the file object to upload

optional params:
    group       - string - uuid of the group to add the image to
    desc        - string - description of the image
    os_variant  - string - rhel5, debian, etc
    os_type     - string - linux, etc
    os_arch     - string - x86, x86_64, etc
    hypervisor  - string - kvm or xen
    owner_r     - bool   - is the image readable by the owner?
    owner_w     - bool   - is the image writeable by the owner?
    group_r     - bool   - is the image readable by the group?
    group_w     - bool   - is the image writeable by the group?
    other_r     - bool   - is the image readable by other?
    other_w     - bool   - is the image writeable by other?

***
## repository/image/{id}
### GET
A GET request on this url will retrieve an object describing the specified image
in detail formatted in json.

each response will be a json object containing:
    uuid        - string - 32 character hex representation of the uuid
    name        - string - the image name
    url         - string - where you can get it from
    owner_uuid  - string -
    group_uuid  - string -
    uploaded    - string -
    modified    - string -
    checksum    - string -
    os_variant  - string -
    os_type     - string -
    os_arch     - string -
    hypervisor  - string -
    permissions - list   - list of bool permissions
    desc        - string -
