import re

from django.core.exceptions import ValidationError
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя(User)."""
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Username указан неверно')
        return data


class UserSignUpSerializer(serializers.Serializer):
    """
    Сериализатор данных для регистрации нового пользователя,
    либо получения кода подтверждения для существующего.
    """
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(email=email, username=username).exists():
            return data

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                'Пользователь с таким email уже зарегистрирован'
            )

        if User.objects.filter(username=username).exists():
            raise ValidationError(
                'Пользователь с таким логином уже зарегистрирован'
            )
        return data

    def validate_username(self, value):
        reg = re.compile(r'^[\w.@+-]+')
        if value == 'me' or not reg.match(value):
            raise ValidationError(
                f'Регистрация пользователя с именем {value} невозможна.'
            )
        return value


class ConfirmationCodeSerializer(serializers.Serializer):
    """Сериализатор данных для получения токена."""
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)
