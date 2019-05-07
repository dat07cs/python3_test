from rest_framework.serializers import *


class NonModelSerializer(Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
