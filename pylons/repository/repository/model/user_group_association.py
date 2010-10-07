# NOT CURRENTLY USED

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Integer

from repository.model.meta import Base

ug_association_table = Table('ug_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('repo_users.id')),
    Column('group_id', Integer, ForeignKey('repo_groups.id')),
    #Column('user_type', Integer, ForeignKey('repo_user_types.id'))
)