from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


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