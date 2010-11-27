from pylons import url


def user(user):
    perms = []
    [perms.extend(g.permissions) for g in user.groups]
    perms = list(set([p.permission_name for p in perms]))
    return {'user_name':user.user_name,
             'full_name':user.full_name,
             'email':user.email,
             'client_dn':user.certificate.client_dn,
             'suspended':user.suspended,
             'permissions':perms,
             'groups':[url('group', group=g.name, qualified=True)
                       for g in user.groups],
             'images':[url('image_by_user', user=user.user_name,
                           image=i.name, qualified=True)
                       for i in user.images]
            }


def group(group):
    return {'name':group.name,
             'permissions':[p.permission_name for p in group.permissions],
             'users':[url('user', user=u.user_name, qualified=True)
                      for u in group.users],
            }


def image(image):
    if image.unauthenticated_access:
        http_url = url('raw_by_user', user=image.owner.user_name,
                       image=image.name, protocol='http')
    else:
        http_url = None

    return {'uuid':image.uuid,
             'name':image.name,
             'owner_user_name':image.owner.user_name,
             'owner':url('user', user=image.owner.user_name, qualified=True),
             'uploaded':ctime_or_none(image.uploaded),
             'modified':ctime_or_none(image.modified),
             'expires':ctime_or_none(image.expires),
             'checksum':{'type':image.checksum.ctype, 'value':image.checksum.cvalue},
             'os_variant':image.os_variant,
             'os_type':image.os_type,
             'os_arch':image.os_arch,
             'hypervisor':image.hypervisor,
             'description':image.description,
             'read_only':image.read_only,
             'unauthenticated_access':image.unauthenticated_access,
             'http_file_url':http_url,
             'raw_file_uploaded':image.raw_uploaded,
             'version':image.version,
             'file_url':url('raw_by_user', user=image.owner.user_name,
                            image=image.name, qualified=True),
             'shared_with':{'groups':[url('group', group=g.name, qualified=True)
                                      for g in image.shared.groups],
                            'users':[url('user', user=u.user_name, qualified=True)
                                      for u in image.shared.users], },
            }

def ctime_or_none(time):
    if time:
        return time.ctime()
    else:
        return None

