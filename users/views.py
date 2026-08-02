from django.contrib.auth import get_user_model

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiResponse,
    extend_schema,
)

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .serializer import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    UserSerializer,
    ChangePasswordSerializer,
)

User = get_user_model()


@extend_schema(
    tags=["Authentication"],
    summary="Register a new user",
    description="""
    Create a new customer account.

    This endpoint is publicly accessible and does not require
    authentication.
    """,
    request=RegisterSerializer,
    responses={
        201: UserSerializer,
        400: OpenApiResponse(description="Validation failed."),
    },
)
class RegisterView(generics.CreateAPIView):
    """
    Register a new user account.
    """

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


@extend_schema(
    tags=["Authentication"],
    summary="Obtain JWT tokens",
    description="""
    Authenticate a user and return a pair of JSON Web Tokens.

    The access token is used to authenticate API requests,
    while the refresh token can be exchanged for a new
    access token when it expires.
    """,
)
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Authenticate a user and issue JWT access and refresh tokens.
    """

    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(
    tags=["Authentication"],
    summary="Refresh an access token",
    description="""
    Exchange a valid refresh token for a new access token.
    """,
)
class CustomTokenRefreshView(TokenRefreshView):
    """
    Refresh an expired JWT access token.
    """

    pass


@extend_schema(
    tags=["Users"],
    summary="Retrieve or update the current user's profile",
    description="""
    Retrieve the authenticated user's profile information
    or update editable profile fields.

    Users can only access and modify their own profile.
    """,
    responses={
        200: UserSerializer,
        401: OpenApiResponse(description="Authentication required."),
    },
)
class MeView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the authenticated user's profile.
    """

    serializer_class = UserSerializer

    def get_object(self):
        """
        Return the currently authenticated user.

        This prevents users from accessing or modifying
        another user's profile.
        """
        return self.request.user


@extend_schema(
    tags=["Users"],
    summary="Change the authenticated user's password",
    description=(
        "Update the password of the currently authenticated user. "
        "The request must include the user's current password and "
        "a new password that satisfies Django's password validation "
        "requirements."
    ),
    request=ChangePasswordSerializer,
    responses={
        200: OpenApiResponse(description="Password changed successfully."),
        400: OpenApiResponse(
            description=(
                "Validation failed because the current password "
                "is incorrect or the new password does not meet "
                "the password policy."
            )
        ),
        401: OpenApiResponse(
            description="Authentication credentials were not provided or are invalid."
        ),
    },
    examples=[
        OpenApiExample(
            "Example request",
            value={
                "old_password": "OldPassword123!",
                "new_password": "NewStrongPassword456!",
            },
            request_only=True,
        ),
    ],
)
class ChangePasswordView(generics.UpdateAPIView):
    """
    Allow an authenticated user to change their account password.

    The endpoint always operates on the currently authenticated
    user rather than accepting a user ID in the URL. This ensures
    users can only change their own passwords.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        """
        Return the authenticated user.

        ``UpdateAPIView`` requires an object to update. Returning
        ``request.user`` ensures that the serializer updates the
        currently authenticated user's password instead of looking
        up a user from a queryset.
        """
        return self.request.user
