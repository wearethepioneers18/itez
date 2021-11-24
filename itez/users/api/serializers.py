from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.fields import ListField

from rolepermissions.roles import assign_role

from ..models import Profile, UserWorkDetail

User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing User password.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        """
        Validates if the fields password and password2 are equal.

        Args:
            attrs [collections.OrderedDict]: Contains data posted in the request body.

        Raises:
            [serializers.ValidationError]: An exception raise when password and password2 don't match.

        Returns:
            attrs [collections.OrderedDict]: Contains data posted in the request body.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        """
        Validates the old_password provided is correct.

        Args:
            value ([str]): Data from the old_password field.

        Raises:
            serializers.ValidationError: This exception is raised if the old_password is not correct.

        Returns:
            [str]: Returns the value if the old_password is correct.
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(required=False)
    class Meta:
        model = Profile
        exclude = ('user',)


class UserWorkDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWorkDetail
        exclude = ('user',)



class UserSerializer(serializers.ModelSerializer):
    roles = ListField(required=False, default=[], write_only=True)
    assigned_roles = serializers.SerializerMethodField(read_only=True)
    profile = UserProfileSerializer(required=False)
    user_work_detail = UserWorkDetailSerializer(required=False)
    class Meta:
        model = User
        fields = [
            "email", 
            "username", 
            "name", 
            "password", 
            "roles", 
            "assigned_roles", 
            "profile", 
            "user_work_detail"
        ]
        extra_kwargs = {
            'email': {'required': False, 'min_length': 8}, 
            'username': {'required': True, 'min_length': 4},
            'name': {'required': True, 'min_length': 8},
            'password': {'required': True, "write_only": True, 'min_length': 8},
        }
        depth = 2
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['username'],
            name=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        roles_to_assign = validated_data.get("roles", [])
        if roles_to_assign:
            for role in roles_to_assign:
                assign_role(user, role)
                
        return user
    
    def get_assigned_roles(self, user):
        return [group.name for group in user.groups.all()]
