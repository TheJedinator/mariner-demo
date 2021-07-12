import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DATE, Table
from sqlalchemy.orm import relationship, backref

from .database import Base

# While this works as a whole, ROLE BASED ACCESS would be the better choice.
# Where roles have permissions and users have roles. this makes thing easier to manage.
# given the task, I didn't veer to far off course and stuck with just permissions in a many to many configuration for
# optimal flexibility, obviously real world this should be wrapped with some business logic...

permission_instance = Table('permission_instance',
                            Base.metadata,
                            Column('user_id', Integer, ForeignKey('users.id')),
                            Column('permission_id', Integer, ForeignKey('permissions.id')),
                            Column('granted_date', DATE, nullable=False, default=datetime.datetime.utcnow)
                            )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    family_name = Column(String, nullable=False)
    given_name = Column(String, nullable=False)
    birthdate = Column(DATE)
    is_active = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)

    permissions = relationship("Permission", secondary=permission_instance, backref=backref('users', lazy='joined'))


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, unique=True)
    display_name = Column(String)
