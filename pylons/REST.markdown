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
/api/groups | GET | display a list of all groups
/api/groups | POST | create a new group based on the POST params
/api/groups/{group} | GET | display the group object for `group`
/api/groups/{group} | DELETE | delete `group`
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

