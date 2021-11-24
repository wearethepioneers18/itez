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
    DestroyModelMixin
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser, JSONParser


from rolepermissions.roles import assign_role
from rolepermissions.roles import RolesManager
from .serializers import (
    UserSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
    UserWorkDetailSerializer
)

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    lookup_field = "id"
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, id=None):
        user = get_object_or_404(User, id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def update(self, request, id=None):
        user_to_update = get_object_or_404(User, id=id)
        data = request.data
        user_to_update.email = data.get('email', user_to_update.email)
        user_to_update.username = data.get('username', user_to_update.username)
        user_to_update.name = data.get('name', user_to_update.name)
        roles_to_assign = data.get("roles", [group.name for group in user_to_update.groups.all()])
        
        user_to_update.groups.clear()
        for role in roles_to_assign:
            assign_role(user_to_update, role)
        
        user_to_update.save()
        serializer = UserSerializer(user_to_update)
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
