from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    FileUploadParser,
    JSONParser,
)


from rolepermissions.roles import assign_role
from rolepermissions.roles import RolesManager
from .serializers import (
    UserSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
    UserWorkDetailSerializer,
)

User = get_user_model()


class UserViewSet(
    GenericViewSet,
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    lookup_field = "id"

    error_message = {"success": False, "msg": "Error updating user"}

    def create(self, request, *args, **kwargs):
        user_id = request.data.get("userID")

        if not user_id:
            raise ValidationError(self.error_message)

        if self.request.user.pk != int(user_id) and not self.request.user.is_superuser:
            raise ValidationError(self.error_message)

        self.update(request)

        return Response({"success": True}, status.HTTP_200_OK)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = User.objects.get(id=request.data.get("userID"))
        roles_to_assign = request.data.get(
            "roles", [group.name for group in instance.groups.all()]
        )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        instance.groups.clear()
        for role in roles_to_assign:
            assign_role(instance, role)

        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get", "put", "patch"])
    def profile(self, request, id=None):
        user = get_object_or_404(User, id=id)
        profile = user.profile
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    @action(detail=True, methods=["get", "put", "patch"])
    def work_details(self, request, id=None):
        user = get_object_or_404(User, id=id)
        work_details = user.user_work_detail

        serializer = UserWorkDetailSerializer(work_details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

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


class RoleAPIView(ViewSet):
    """
    API endpoint to list All available and roles.
    """

    def list(self, request):
        roles = RolesManager.get_roles_names()
        return Response({"roles": roles})
