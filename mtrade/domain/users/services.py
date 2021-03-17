# python imports
from typing import Type

from django.db.models.signals import post_save

# django imports
from django.db.models.manager import Manager

from .models import UserFactory
from .models import User


class UserServices():

    @staticmethod
    def get_user_factory():
        return UserFactory

    @staticmethod
    def get_user_repo():
        return User.objects


#    @staticmethod
#    def subscribe_to_user_post_save(handler, dispatch_uid):
#        post_save.connect(handler, sender=User, dispatch_uid = dispatch_uid, weak=False)
