from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from users.permissions import AdminPermission
from users.serializers import (ConfirmationCodeSerializer, UserSerializer,
                               UserSignUpSerializer)

CONFIRM_EMAIL_SUBJECT = 'Вош код подтверждения'
CONFIRM_EMAIL_SENDER = settings.DEFAULT_FROM_EMAIL


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Пользователи (UserManage)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'patch', 'delete', 'post']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
        url_name='me',
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put_validate(self, request):
        raise MethodNotAllowed('PUT')


@api_view(['POST'])
def signup_user(request):
    """Вью функция регистрации новых пользователей"""
    serializer = UserSignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user, _created = User.objects.get_or_create(
        username=username,
        email=email
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        CONFIRM_EMAIL_SUBJECT,
        f'{CONFIRM_EMAIL_SUBJECT} : {confirmation_code}',
        CONFIRM_EMAIL_SENDER,
        [email],
        fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    """Вью функция аутентификации пользователей"""
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    confirmation_code = serializer.validated_data['confirmation_code']
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(
            'Токен не валиден',
            status=status.HTTP_400_BAD_REQUEST
        )
    user_token = {'token': str(AccessToken.for_user(user))}
    return Response(user_token, status=status.HTTP_200_OK)
