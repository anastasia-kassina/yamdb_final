import re

from rest_framework import serializers
from django.utils import timezone
from django.shortcuts import get_object_or_404

from reviews.models import (
    User, Category, Genre, Title, Review, Comment
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class PersonalSerializer(UserSerializer):
    """Сериализатор для пользователя."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                "Array of strings"
            )
        return data


class ValidationSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField()
    username = serializers.CharField(
        required=True, allow_null=True,
        allow_blank=True
    )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'

    def validate_slug(self, value):
        """Проверка соответствия слага жанра."""
        if not re.fullmatch(r'^[-a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                'Псевдоним жанра не соотвествует формату',
            )
        return value


class TitleSerializer(serializers.ModelSerializer):
    """Базовый сериализатор модели Title."""

    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )

    def validate_year(self, value):
        """Проверка года."""
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                'Такой год %(value)s еще не наступил!',
                params={'value': value},
            )
        return value


class TitleReadSerializer(TitleSerializer):
    """Сериализатор модели Title для чтения."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)


class TitleWriteSerializer(TitleSerializer):
    """Сериализатор модели Title для записи."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False,
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )


class ReviewSerializers(serializers.ModelSerializer):
    """Сериалайзер для работы с моделями отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context.get('request')
        if request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(
                author=request.user, title=title
            ):
                raise serializers.ValidationError(
                    'Ограничение количества отзывов!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с моделями отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only = ('review',)
