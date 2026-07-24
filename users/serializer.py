from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)

from cart.models import Cart


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Validate input and create a new user account.

    The serializer applies Django's configured password validators
    and creates an empty shopping cart for the new user.
    """

    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        )

    def validate_password(self, value):
        """
        Validate the password using Django's configured password
        validation framework.
        """
        validate_password(value)
        return value

    def create(self, validated_data):
        """
        Create a new user and initialize their shopping cart.

        Every registered customer owns exactly one cart, allowing
        them to begin shopping immediately after registration.
        """
        password = validated_data.pop("password")
        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        # Registration may be retried safely. If a cart already exists,
        # reuse it instead of creating a duplicate.
        Cart.objects.get_or_create(user=user)

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customize the JWT payload returned during authentication.

    This serializer currently preserves the default Simple JWT
    behavior, but it provides a convenient extension point for
    adding custom claims in the future.
    """

    @classmethod
    def get_token(cls, user):
        """
        Generate a JWT for the authenticated user.

        Override this method to include additional claims if
        required by the application.
        """
        token = super().get_token(user)
        return token


class UserSerializer(serializers.ModelSerializer):
    """
    Serialize the authenticated user's profile information.
    """

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "address",
        )
