from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password, password_changed

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


class ChangePasswordSerializer(serializers.Serializer):
    """
    Validate and update the authenticated user's password.

    The serializer requires the user's current password and a new password.
    It verifies that the current password is correct, validates the new
    password against Django's configured password validators, and updates
    the user's password if all validation succeeds.
    """

    old_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        trim_whitespace=False,
        help_text="The user's current password.",
    )

    new_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        trim_whitespace=False,
        help_text=(
            "The new password. It must satisfy Django's configured "
            "password validation rules."
        ),
    )

    def validate_old_password(self, value):
        """
        Ensure the supplied current password matches the user's
        existing password.

        This method is called automatically by DRF during
        ``serializer.is_valid()``.
        """
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError("The current password is incorrect.")

        return value

    def validate_new_password(self, value):
        """
        Validate the proposed new password.

        Django's password validation framework checks requirements
        such as minimum length, similarity to user information,
        common passwords, and numeric-only passwords (depending on
        project settings).
        """
        validate_password(value)
        return value

    def save(self):
        """
        Replace the authenticated user's password.

        This method should be called only after successful validation.
        The serializer updates the user's password using Django's
        ``set_password()`` method, which securely hashes the password
        before saving it to the database.

        After the password is changed, Django's password validators
        are notified through ``password_changed()``.
        """
        # The instance is supplied by UpdateAPIView via get_object().
        user = self.instance

        # Retrieve the validated new password.
        password = self.validated_data["new_password"]

        # Hash the password and assign it to the user.
        user.set_password(password)

        # Persist the updated password hash.
        user.save()

        # Notify Django's password validation framework that the
        # password has been successfully changed.
        password_changed(password, user)

        return user
