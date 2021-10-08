from rest_framework import serializers
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'address']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create(first_name = validated_data['first_name'], last_name = validated_data['last_name'], email=validated_data['email'], address=validated_data['address'])
        user.set_password(validated_data['password'])
        user.save()
        return user