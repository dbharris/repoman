from repository.model.meta import Session, Base
from repository.model.permission import Permission
from repository.model.group import Group

from repository import model
from os import path

# hard code for now.  read in from config soon.
all_perms = [
    #user related permissions
    'user_create',
    'user_modify',
    'user_delete',
    'user_list_all',
    'user_modify_self',
    #group related permissions
    'group_create',
    'group_modify',
    'group_delete',
    'group_list_all',
    'group_modify_membership',
    #image related permissions
    'image_create_owned',
    'image_modify_owned',
    'image_delete_owned',
    'image_list_all',
    'image_modify_group',
    'image_delete_group',
    'image_modify_any',
    'image_delete_any'
    ]

default_groups = {'admins':all_perms,
                  'users':['user_modify_self',
                           'image_create_owned',
                           'image_modify_owned',
                           'image_delete_owned'],
                  'users_admins':['group_modify',
                                  'group_modify_membership',
                                  'image_modify_group',
                                  'image_delete_group'],
                 }


def create(conf):
    permissions = {}
    groups = []

    # create permissions
    for p in all_perms:
        new_p = Permission(p)
        Session.add(new_p)
        permissions.update({p:new_p})

    for g,perms in default_groups.iteritems():
        new_g = Group(g)
        new_g.protected = True
        for p in perms:
            new_g.permissions.append(permissions[p])

    admins = Session.query(Group).filter(Group.name=='admins').first()

    # add some users from a file into the db for testing
    # each line of the file should be of the form name,email,dn
    admin_file = conf.global_conf['admin_file']
    f = open(path.expandvars(admin_file), 'r')
    for line in f:
        name, email, dn = line.rstrip('\n').split(',')
        user = model.User(user_name=name, email=email, cert_dn=dn)
        user.suspended=False
        user.groups.append(admins)
        Session.add(user)
    f.close()
    Session.commit()

