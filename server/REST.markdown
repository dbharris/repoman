# RESTfull API

## URL Summary

URL | HTTP_METHOD | DESCRIPTION |
:---|:------------|:------------|
/api/whoami | GET | display the user object of the currently logged in user
/api/users | GET | display a list of all users
/api/users | POST | create a new user based on PORT params
/api/users/{user} | GET | display the user object for `user`
/api/users/{user} | POST | modify the user object for `user`
/api/users/{user} | DELETE | delete `user`
/api/users/{user}/shared | GET | get a list of images shared with `user`
/api/groups | GET | display a list of all groups
/api/groups | POST | create a new group based on the POST params
/api/groups/{group} | GET | display the group object for `group`
/api/groups/{group} | DELETE | delete `group`
/api/groups/{group} | POST | modify `group`
/api/groups/{group}/users | GET | display a list of users who are members of `group`
/api/groups/{group}/users/{user} | POST | add `user` to `group`
/api/groups/{group}/users/{user} | DELETE | remove `user` from `group`
/api/groups/{group}/permissions | GET | display a list of permissions for `group`
/api/groups/{group}/permissions/{permission} | POST | add `permission` to `group`
/api/groups/{group}/permissions/{permission} | DELETE | remove `permission` from `group`
/api/images | GET | display a list of all images
/api/images | POST | create an image owned by the currently logged in user
/api/images/{image} | GET | display metadata for `image` in the current users namespace
/api/images/{image} | POST | modify metadata for `image` in the current users namespace
/api/images/{image} | DELETE | delete `image` in the current users namespace
/api/images/{user}/{image} | GET | display metadata for `image` in namespace of `user`
/api/images/{user}/{image} | POST | modify metadata for `image` in namespace of `user`
/api/images/{user}/{image} | DELETE | delete `image` in namespace of `user`
/api/images/raw/{image} | GET | get the raw image file that belongs to `image` in the current users namespace
/api/images/raw/{image} | POST | upload the raw image file that belongs to `image` in the current users namespace
/api/images/raw/{user}/{image} | GET | get the raw image file that belongs to `image` in the namespace of `user`
/api/images/raw/{user}/{image} | POST | upload the raw image file that belongs to `image` in the namespace of `user`
/api/images/{user}/{image}/share/user/{share_with} | POST | share `image` in the namespace of `user` with `share_with` user
/api/images/{user}/{image}/share/user/{share_with} | DELETE | unshare `image` in the namespace of `user` with `share_with` user
/api/images/{user}/{image}/share/group/{share_with} | POST | share `image` in the namespace of `user` with `share_with` group
/api/images/{user}/{image}/share/group/{share_with} | DELETE | unshare `image` in the namespace of `user` with `share_with` group
/api/images/{image}/share/user/{share_with} | POST | share `image` in the current users namespace with `share_with` user
/api/images/{image}/share/user/{share_with} | DELETE | unshare `image` in current users namespace with `share_with` user
/api/images/{image}/share/group/{share_with} | POST | share `image` in current users namespace with `share_with` group
/api/images/{image}/share/group/{share_with} | DELETE | unshare `image` in current users namespace with `share_with` group


## Creating Users
To create a user POST to `/api/users`.

Param | Type | Required | Description |
:-----|:-----|:--------:|:------------|
user_name | String | yes | the repoman-wide unique user name for this user
email | String | yes | a valid email for the user
cert_dn | String | yes | the users certificate distinguished name
full_name | String | yes | full name for the user

**Http Status Codes**

Code | Occurs When | Response Body |
:----|:------------|:--------------|
200 | user was created with no problems | json representation of user
400 | bad set of paramaters was supplied | -
409 | conflicting user_name of client_dn | -


## Creating Groups
To create a group POST to `/api/groups`.

Param | Type | Required | Description |
:-----|:-----|:--------:|:------------|
name | String | yes | the repoman-wide unique name for this group

**Http Status Codes**

Code | Occurs When | Response Body |
:----|:------------|:--------------|
200 | group was created with no problems | json representation of group
400 | bad set of paramaters was supplied | -
409 | conflicting name for group | -


## Creating Images
To create an image POST to `/api/images`.

Param | Type | Required | Description |
:-----|:-----|:--------:|:------------|
name | String | yes | image name unique to the users namespace
description | String | no | description of the image
os_variant | String | no | redhat, centos, ubuntu, etc.
os_arch | String | no | x86, x86_64
os_type | String | no | linux, unix, windows, etc.
hypervisor | String | no | kvm, xen
read_only | Bool | no | should the image be readonly?

**Http Status Codes**

Code | Occurs When | Response Body | Other |
:----|:------------|:--------------|:------|
201 | image metadata object was created | json representation of image | `Location` header contains url to upload raw image at
400 | bad set of paramaters was supplied | - | -
409 | conflict image name in the namespace | - | -


## Uploading an image file
To upload a image file POST to `/api/images/raw/{image}` or '/api/images/raw/{user}/image'

Param | Type | Required | Description |
:-----|:-----|:--------:|:------------|
file | form_file | yes | a standard file post field that contains your image


**Http Status Codes**

Code | Occurs When | Response Body |
:----|:------------|:--------------|
200 | image file uploaded ok | -
400 | bad set of paramaters was supplied | -

## Modifying an existing Image
To modify the metadata for an existing image POST to `/api/images/{image}` or `/api/images/{user}/{image}`
Only the paramaters that are specified will be overwritten.

Param | Type | Required | Description |
:-----|:-----|:--------:|:------------|
name | String | no| image name unique to the users namespace
description | String | no | description of the image
os_variant | String | no | redhat, centos, ubuntu, etc.
os_arch | String | no | x86, x86_64
os_type | String | no | linux, unix, windows, etc.
hypervisor | String | no | kvm, xen
read_only | Bool | no | should the image be readonly?

