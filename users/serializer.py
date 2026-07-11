from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from cart.models import Cart

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "address",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        # Registration may be retried; do not create duplicate carts.
        Cart.objects.get_or_create(user=user)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # These claims are safe display/role hints, never private customer data.
        token["username"] = user.username
        token["is_staff"] = user.is_staff
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "phone_number", "address")
