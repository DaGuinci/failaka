from rest_framework.serializers import (
    ModelSerializer,
    ValidationError
    )

from authentication.models import User
from django.contrib.auth.models import Group


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
            ]
        extra_kwargs = {"password": {"write_only": True}}

    def __str__(self):
        return self.email


class RegisterSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password'
            )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user with this email already exists.")
        return value


    def create(self, validated_data):
        # set default group to visitor

        user = User.objects.create(
            first_name=validated_data['first_name'] if 'first_name' in validated_data else '',
            last_name=validated_data['last_name'] if 'last_name' in validated_data else '',
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()
        user.groups.add(Group.objects.get(name='visitors'))

        return user

class UpdateUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user with this email already exists.")
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)

        instance.save()

        return instance