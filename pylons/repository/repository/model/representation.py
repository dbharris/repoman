#
# Contains the representation of objects stored in the database
# Each object should have at least two represenations
#
# REQUIRED
#   * Long  - This should contain all information about an object that
#             a user would consider relevant
#
#   * Short - This should contain only a small subset of information about as
#             object.  At the minimum it needs to contain the object UUID and
#             one other descriptor such as a name.
#
# OPTIONAL
#   * Full  - This should contain ALL information about an object.  Access and
#             usage of these representations should be restricted to admins
#             and administration tasks.
#
#
# The Long representation will be used when an object is referenced directly.
# The Short representatin will be used when referencing the collection
#
# Naming convensions:
#   functions names should be of the form <object><short|long|full>
#   Examples:
#       def user_short(*obj):
#           pass
#
#       def user_long(*obj):
#           pass

import simplejson as json

#################
#   U S E R S   #
#################

def user_short(*obj):
    data = []
    for u in obj:
        data.append({'user_name':u.user_name,
                     'full_name':u.full_name,
                     'email':u.email,
                     'client_dn':u.certificate.client_dn,
                    })
    if len(data) == 1:
        return data[0]
    else:
        return data


def user_long(*obj):
    data = []
    for user in obj:
        data.append({'user_name':user.user_name,
                     'full_name':user.full_name,
                     'email':user.email,
                     'client_dn':user.certificate.client_dn,
                     'suspended':user.suspended,
                     'quota':[None],
                     'images':[image_short(i) for i in user.images],
                     'groups':[group_short(g) for g in user.groups],
                    })
    if len(data) == 1:
        return data[0]
    else:
        return data




###################
#   I M A G E S   #
###################

def image_short(*obj):
    data = []
    for i in obj:
        data.append({'id':i.uuid,
                     'name':i.name,
                     'owner':i.owner.user_name,
                     'group':i.group.name,
                    })
    if len(data) == 1:
        return data[0]
    else:
        return data

def image_long(*obj):
    data = []
    for image in obj:
        data.append({'id':image.uuid,
                     'name':image.name,
                     'url':image.url,
                     'owner':image.owner.user_name,
                     'group':image.group.name,
                     'uploaded':image.uploaded.ctime(),
                     'modified':image.modified.ctime(),
                     'checksum':image.checksum,
                     'os_variant':image.os_variant,
                     'os_type':image.os_type,
                     'os_arch':image.os_arch,
                     'hypervisor':image.hypervisor,
                     'permissions':{'owner_r':image.owner_r,
                                    'owner_w':image.owner_w,
                                    'group_r':image.group_r,
                                    'other_r':image.other_r},
                     'desc':image.desc,
                    })
    if len(data) == 1:
        return data[0]
    else:
        return data



###################
#   G R O U P S   #
###################

def group_short(*obj):
    data = []
    for g in obj:
        data.append({'name':g.name})
    if len(data) == 1:
        return data[0]
    else:
        return data

def group_long(*obj):
    data = []
    for group in obj:
        data.append({'name':group.name,
                     'protected':group.protected,
                     'permissions':[p.permission_name for p in group.permissions],
                     'users':[user_short(u) for u in group.users]
                    })
    if len(data) == 1:
        return data[0]
    else:
        return data

