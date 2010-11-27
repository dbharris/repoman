from repoman.model.meta import Session, Base
from repoman.model.permission import Permission
from repoman.model.group import Group

from repoman import model
from os import path
from time import time
from datetime import datetime

# hard code for now.  read in from config soon.
all_perms = [
    #user related permissions
    'user_create',
    'user_modify',
    'user_delete',
    'user_modify_self',
    #group related permissions
    'group_create',
    'group_modify',
    'group_delete',
    'group_modify_membership',
    'group_modify_permissions',
    #image related permissions
    'image_modify_group',
    'image_delete_group',
    'image_create',
    'image_delete',
    'image_modify',
    ]

default_groups = {'admins':all_perms,
                  'users':['user_modify_self',
                           'image_create',
                          ]
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
        Session.add(new_g)

    Session.commit()

    admins = Session.query(Group).filter(Group.name=='admins').first()
    # add some users from a file into the db for testing
    # each line of the file should be of the form name,email,dn
    admin_file = conf.global_conf['admin_file']
    f = open(path.expandvars(admin_file), 'r')
    for line in f:
        name, email, dn = line.rstrip('\n').split(',')
        user = model.User(user_name=name, email=email, cert_dn=dn)
        user.suspended=False
        user.deleted=False
        current_time = datetime.utcfromtimestamp(time())
        user.created = current_time
        user.groups.append(admins)
        Session.add(user)
    f.close()
    Session.commit()

