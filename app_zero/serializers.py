from lib.django.custom_serializers import ApplicationModelSerializer

def buildDefaultAppZeroSerializer(model_class, services_class):

    class cls(ApplicationModelSerializer):

        def create_from_app_service(self, user, validated_data):
            # this method links the interface layer with the application layer
            # The returned instance comes from the application layer, not the
            # domain layer
            return services_class.create_resource_from_dict(user, validated_data)

        def update_from_app_service(self, user, instance, validated_data):
            # This method links the interface layer with the application layer
            # The returned instance comes from the application layer, not the
            # domain layer
            return services_class.update_resource_from_dict(user, instance, validated_data)

        class Meta:
            model = model_class
            fields = '__all__'

    cls.__name__ = model_class.__name__+'AppZeroSerializer'

    return cls
