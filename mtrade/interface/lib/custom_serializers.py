import traceback

from rest_framework import serializers
from rest_framework.utils import model_meta

from lib.ddd.exceptions import VOValidationExcpetion
from mtrade.interface.lib.base_responses import BadRequest


class ApplicationModelSerializer(serializers.ModelSerializer):

    def create_from_app_service(self, validated_data):
        """
        The build_instance method should transform validated data into domain
        value objects that should be passed to an application service
        """
        raise NotImplementedError('`create_from_app_service()` must be implemented.')

    def update_from_app_service(self, instance, validated_data):
        """
        The build_instance method should transform validated data into domain
        value objects that should be passed to an application service
        """
        raise NotImplementedError('`update_from_app_service()` must be implemented.')

    def get_user(self):
        request = self.context.get('request', None)
        if not request:
            return None
        if not request.user:
            return None
        return request.user

    def create(self, validated_data):
        """
        This method is based on ModelSerializer's create method. It
        replaces direct calls to model creation with calls that go through
        the application layer.
        """
        serializers.raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        instance = None
        try:
            instance = self.create_from_app_service(validated_data)
        except VOValidationExcpetion as ve:
            raise BadRequest(ve)
        #TODO: Check if handling for TypeError is still necessary
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # TODO: Verify this doesn't write directly to models
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance

    def update(self, instance, validated_data):
        """
        This method is based on ModelSerializer's update method. It
        replaces direct calls to model creation with calls that go through
        the application layer.
        """
        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        # Original block
        # instance.save()
        # Replacement block
        updated_instance = None
        try:
            updated_instance = self.update_from_app_service(instance, validated_data)
        except VOValidationExcpetion as ve:
            raise BadRequest(ve)

        for attr, value in m2m_fields:
            field = getattr(updated_instance, attr)
            field.set(value)

        return updated_instance
