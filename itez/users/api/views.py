from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import (
    UserSerializer,
    ChangePasswordSerializer,
    GroupModelSerializer
)

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ChangePasswordView(UpdateModelMixin, GenericViewSet):
    """
    API end point for changing password on User model.
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class RoleAPIView(ListModelMixin,RetrieveModelMixin, 
    CreateModelMixin, UpdateModelMixin, 
    GenericViewSet, DestroyModelMixin
    ):
    """
    API endpoint for Group model to list, create, update and delete.
    """
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

