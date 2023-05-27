import reviews.models as model
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели категории(Category)"""
    class Meta:
        model = model.Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели жанра(Genre)"""
    class Meta:
        model = model.Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор чтения модели произведения(Title)"""
    genre = GenreSerializer(many=True, required=True)
    category = CategorySerializer(required=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return obj.rating

    class Meta:
        model = model.Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор записи модели произведения(Title)"""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=model.Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=model.Category.objects.all()
    )

    class Meta:
        model = model.Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментария(Comment)"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = model.Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзыва(Review)"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(model.Title, pk=title_id)
        if title.reviews.filter(author=request.user).exists():
            raise ValidationError(
                'Допустимо не более 1 отзыва на произведение')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = model.Review
