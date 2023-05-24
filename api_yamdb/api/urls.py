from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CreateUserView, UserViewSet,
    CategoryViewSet, GenreViewSet,
    TitleViewSet, ReviewViewSet, CommentViewSet,
    UserValidationView
)


router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register(
    'categories',
    CategoryViewSet,
    basename='category',
)
router.register(
    'genres',
    GenreViewSet,
    basename='genre',
)
router.register(
    'titles',
    TitleViewSet,
    basename='title',
)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='Review'
)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='Comment'
)


urlpatterns = [
    path('v1/auth/signup/', CreateUserView, name='create_user'),
    path('v1/', include(router.urls)),
    path('v1/auth/token/', UserValidationView, name='user_validation'),
]
