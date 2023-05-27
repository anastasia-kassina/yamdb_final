import api.serializers as sl
import reviews.models as model
from api.filters import TitleFilter
from api.viewsets import ViewCreateDeleteViewSet
from django.db import models
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from users.permissions import (AdminModeratorAuthorPermission,
                               AdminOrReadOnlyPermission)


class CategoryViewSet(ViewCreateDeleteViewSet):
    """Вьюсет для модели категории (Category)"""
    queryset = model.Category.objects.all()
    serializer_class = sl.CategorySerializer
    permission_classes = [AdminOrReadOnlyPermission]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ViewCreateDeleteViewSet):
    """Вьюсет для модели жанр (Genre)"""
    queryset = model.Genre.objects.all()
    serializer_class = sl.GenreSerializer
    permission_classes = [AdminOrReadOnlyPermission]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели произведение (Title)"""
    queryset = model.Title.objects.annotate(
        rating=models.Avg('reviews__score')
    ).order_by('year', 'name')
    permission_classes = [AdminOrReadOnlyPermission]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return sl.TitleReadSerializer
        return sl.TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели отзыва (Review)"""
    serializer_class = sl.ReviewSerializer
    permission_classes = [AdminModeratorAuthorPermission]

    def get_queryset(self):
        title = get_object_or_404(model.Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(model.Title, id=title_id)
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели комментария (Comment)"""
    serializer_class = sl.CommentSerializer
    permission_classes = [AdminModeratorAuthorPermission]

    def get_queryset(self):
        review = get_object_or_404(
            model.Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            model.Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
