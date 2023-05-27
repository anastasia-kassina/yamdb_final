from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ViewCreateDeleteViewSet(mixins.CreateModelMixin,
                              mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              GenericViewSet):
    """
    Вьюсет, обеспечивающий просмотр списка, добавление и удаление элементов
    """
