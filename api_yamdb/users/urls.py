from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, get_jwt_token, signup_user

router = DefaultRouter()
router.register('users', UserViewSet)

auth_pattern = [
    path('signup/', signup_user, name='signup_user'),
    path('token/', get_jwt_token, name='get_jwt_token'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(auth_pattern)),
]
