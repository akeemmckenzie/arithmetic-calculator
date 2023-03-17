from rest_framework import serializers
from .models import CustomUser, Operation, Record

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', "credit")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = '__all__'

class RecordSerializer(serializers.ModelSerializer):
    operation_type = serializers.StringRelatedField(source='operation.type')

    class Meta:
        model = Record
        fields = '__all__'
        extra_fields = ('operation_type',)
