
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Integer

from repoman.model.meta import Base

# User group membership
# many-to-many relationship
user_group_association = Table('user_group_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('group_id', Integer, ForeignKey('group.id')),
)

# Group permissions
# Many-to-many relationship
group_permission_association = Table('group_permission_association', Base.metadata,
    Column('group_id', Integer, ForeignKey('group.id')),
    Column('permission_id', Integer, ForeignKey('permission.id')),
)

## Image sharing
# many-to-many relationship
imageshare_user_association = Table('imageshare_user_association', Base.metadata,
    Column('imageshare_id', Integer, ForeignKey('image_share.id')),
    Column('user_id', Integer, ForeignKey('user.id')),
)

## Image sharing
# many-to-many relationship
imageshare_group_association = Table('imageshare_group_association', Base.metadata,
    Column('imageshare_id', Integer, ForeignKey('image_share.id')),
    Column('group_id', Integer, ForeignKey('group.id')),
)

