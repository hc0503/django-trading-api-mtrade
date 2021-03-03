# python import
from typing import Type

# django imports
from django.db.models.query import QuerySet

class DefaultAppZeroServices():

    def __init__(self, model_class: Type):
        self.model_class = model_class

    def list_resources(self, user) -> QuerySet:
        return self.model_class.objects.all()

    def create_resource_from_dict(self, user, data: dict):
        try:
            instance = self.model_class._default_manager.create(**data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create_resource_from_dict() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    self.model_class.__name__,
                    self.model_class._default_manager.name,
                    self.model_class.__name__,
                    self.model_class._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)
        return instance

    def update_resource_from_dict(self, user, instance, data: dict):
        for attr, value in data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
