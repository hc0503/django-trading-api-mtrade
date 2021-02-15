import uuid
from dataclasses import dataclass, field

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from lib.data_manipulation.type_conversion import asdict


class UserManagerAutoID(UserManager):
    """
    A User Manager that sets the uuid on a model when calling the create_superuser function.
    """
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if id not in extra_fields:
            extra_fields = dict(extra_fields, id = UserID().id)

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """
    A User replaces django's default user id with a UUID that should be created by the application, not the database.
    """
    id = models.UUIDField(primary_key=True, editable=False)

    objects = UserManagerAutoID()


@dataclass(frozen=True)
class UserID():
    """
    This is a value object that should be used to generate and pass the UserID to the UserFactory
    """
    id: uuid.UUID = field(init=False, default_factory=uuid.uuid4)


@dataclass(frozen=True)
class UserPersonalData():
    """
    This is a value object that should be used to pass user personal data to the UserFactory
    """
    username: str
    first_name: str
    last_name: str
    email: str


@dataclass(frozen=True)
class UserBasePermissions():
    """
    This is a value object that should be used to pass user base permissions to the UserFactory
    """
    is_staff: bool
    is_active: bool


class UserFactory():
    @staticmethod
    def build_entity_with_id(personal_data: UserPersonalData, base_permissions: UserBasePermissions):
        personal_data_dict = asdict(personal_data, skip_empty=True)
        base_permissions_dict = asdict(base_permissions, skip_empty=True)
        return User(id=UserID().id, **personal_data_dict, **base_permissions_dict)
