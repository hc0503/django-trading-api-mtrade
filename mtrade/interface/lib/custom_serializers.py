import traceback

from rest_framework import serializers
from rest_framework.utils import model_meta


class ApplicationModelSerializer(serializers.ModelSerializer):

    def build_instance(self, validated_data):
        """
        The build_instance method should transform validated data into domain
        value objects that should be passed to an application service
        """
        raise NotImplementedError('`build_instance()` must be implemented.')

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

        try:
            # Original block
            # instance = ModelClass._default_manager.create(**validated_data)
            # Replacement block
            instance = self.build_instance(validated_data)
            instance.save()
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
        raise_errors_on_nested_writes('update', self, validated_data)
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
        instance = self.build_instance(validated_data)
        instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance
