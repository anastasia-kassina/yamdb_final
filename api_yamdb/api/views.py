from django.contrib.auth.tokens import (
    PasswordResetTokenGenerator,
    default_token_generator
)
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework import (
    response, status,
    viewsets, filters, mixins
)
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    AllowAny,
    SAFE_METHODS,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly
from reviews.models import User, Category, Genre, Title, Review
from .permissions import IsAdminUser, AuthorAdminModeratorOrReadOnly
from .serializer import (
    CreateUserSerializer, UserSerializer,
    ValidationSerializer, CategorySerializer,
    GenreSerializer, TitleReadSerializer,
    TitleWriteSerializer, ReviewSerializers,
    CommentSerializer, PersonalSerializer
)


def user_send_code(user):
    confirmation_code = default_token_generator.make_token(user)
    return send_mail(
        'confirmation_code',
        f'confirmation_code: {confirmation_code}',
        settings.DEFAULT_EMAIL,
        [user.email],
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def CreateUserView(request):
    if User.objects.filter(
        username=request.data.get('username'),
        email=request.data.get('email')
    ).exists():
        user, _ = User.objects.get_or_create(
            username=request.data.get('username'),
            email=request.data.get('email')
        )
        user_send_code(user)
        return Response(
            'Токен обновлен',
            status=status.HTTP_200_OK
        )
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    user_send_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def UserValidationView(request):
    serializer = ValidationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if not PasswordResetTokenGenerator().check_token(user, confirmation_code):
        return response.Response(
            'Отсутствует обязательно поле или оно некоректно',
            status=status.HTTP_400_BAD_REQUEST
        )
    token = RefreshToken.for_user(user)
    return Response(
        {'token': str(token.access_token)},
        status=status.HTTP_200_OK
    )


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ['username']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = PersonalSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(
                serializer.data, status=status.HTTP_200_OK
            )
        serializer = PersonalSerializer(user)
        return response.Response(
            serializer.data, status=status.HTTP_200_OK
        )


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Дженерик для операций retrieve/create/list."""

    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )


class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score'),
    ).order_by('name')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(ModelViewSet):
    """Вьюсет для работы с отзывами."""

    serializer_class = ReviewSerializers
    permission_classes = [AuthorAdminModeratorOrReadOnly]
    pagination_class = PageNumberPagination

    def _get_title(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        queryset = self._get_title().reviews.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self._get_title()
        )


class CommentViewSet(ModelViewSet):
    """Вьюсет для работы с комментариями"""

    serializer_class = CommentSerializer
    permission_classes = [AuthorAdminModeratorOrReadOnly]

    def _get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self._get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self._get_review()
        )
