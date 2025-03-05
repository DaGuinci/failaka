from rest_framework.serializers import (
    ModelSerializer,
    ValidationError
    )

from authentication.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
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
            'role',
            'password'
            )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user with this email already exists.")
        return value


    def create(self, validated_data):
        # set default role to visitor
        validated_data['role'] = 'visitor'

        user = User.objects.create(
            first_name=validated_data['first_name'] if 'first_name' in validated_data else '',
            last_name=validated_data['last_name'] if 'last_name' in validated_data else '',
            email=validated_data['email'],
            role=validated_data['role']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user