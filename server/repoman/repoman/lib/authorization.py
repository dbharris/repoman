#
# Much of the code in this file is taken from the pylons cookbook at:
# http://wiki.pylonshq.com/display/pylonscookbook/Another+approach+for+authorization+in+pylons+(decorator+based,+repoze.what+like)
#

# easy_install decorator
from decorator import decorator

from pylons import request

from repoman.model import meta
from repoman.model.group import Group
from repoman.model.user import User
from repoman.model.permission import Permission




#######################
# C O N D I T I O N S #
#######################

class MemberOf(object):
    invalid_group_message = u'Group does not exist'
    message = u'User must be a member of the specified group'

    def __init__(self, group):
        self.group_name = group

    def check(self):
        user = request.environ.get('REPOMAN_USER')
        group = meta.Session.query(Group).filter(Group.name==self.group_name).first()
        if not group:
            raise NotValidAuth(self.invalid_group_message)
        elif group in user.groups:
            return True
        else:
            raise NotValidAuth(self.message)


class HasPermission(object):
    def __init__(self, permission):
        self.permission_name = permission
        self.message = u"Required permission: '%s'" % permission
        self.invalid_permission_message = u"Required permission does not exist: '%s'" % permission

    def check(self):
        user = request.environ.get('REPOMAN_USER')
        permission = meta.Session.query(Permission).filter(Permission.permission_name==self.permission_name).first()
        if not permission:
            raise NotValidAuth(self.invalid_permission_message)
        else:
            for g in user.groups:
                if permission in g.permissions:
                    return True
        raise NotValidAuth(self.message)


class OwnsImage(object):
    pass


class LoggedIn(object):
    """This condition is somewhat useless at the moment.  a user is either
    implicitly logged in, or they have no access to the api."""

    message = u'User must be logged in'

    def check(self):
        user = request.environ.get('REPOMAN_USER')
        if user:
            return True
        else:
            raise NotValidAuth(self.message)

###################
# C H E C K E R S #
###################
class AllOf(object):

    message = u'All of these conditions have to be met: %s.'

    def __init__(self, *args):
        self.conditions = args

    def check(self):
        condition_messages = []
        valid = True
        for condition in self.conditions:
            try:
                condition.check()
            except NotValidAuth, e:
                valid = False
                condition_messages.append(unicode(e))
        if valid:
            return True
        raise NotValidAuth(self.message % ', '.join(condition_messages))


class AnyOf(object):

    message = u'At least one of these conditions have to be met: %s.'

    def __init__(self, *args):
        self.conditions = args

    def check(self):
        condition_messages = []
        valid = False
        for condition in self.conditions:
            try:
                condition.check()
                return True
            except NotValidAuth, e:
                condition_messages.append(unicode(e))
        raise NotValidAuth(self.message % ', '.join(condition_messages))


class NoneOf(object):
    message = u'All of these conditions have to be not met: %s.'

    def __init__(self, *args):
        self.conditions = args

    def check(self):
        condition_messages = []
        valid = True
        for condition in self.conditions:
            try:
                condition.check()
                valid = False
            except NotValidAuth, e:
                condition_messages.append(unicode(e))
        if valid:
            return True
        raise NotValidAuth(self.message % ', '.join(condition_messages))


#######################
# D E C O R A T O R S #
#######################

def authorize(valid, handler):
    def validate(func, self, *args, **kwargs):
        try:
            valid.check()
        except NotValidAuth, e:
            return handler(e)
        else:
            return func(self, *args, **kwargs)

    return decorator(validate)

#######################
# E X C E P T I O N S #
#######################

class NotValidAuth(Exception):
    pass

