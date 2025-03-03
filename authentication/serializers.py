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
        return self.username


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

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user with this email already exists.")
        return value


    def create(self, validated_data):
        # check role is not null
        if 'role' not in validated_data or validated_data['role'] not in ['admin', 'valid']:
            validated_data['role'] = 'norole'

        user = User.objects.create(
            first_name=validated_data['first_name'] if 'first_name' in validated_data else '',
            last_name=validated_data['last_name'] if 'last_name' in validated_data else '',
            email=validated_data['email'],
            role=validated_data['role']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user