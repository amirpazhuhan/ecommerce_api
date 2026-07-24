from django.contrib.auth import get_user_model

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)

from rest_framework import generics
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .serializer import (
    CustomTokenObtainPairSerializer,
    RegisterSerializer,
    UserSerializer,
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
        400: OpenApiResponse(
            description="Validation failed."
        ),
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
        401: OpenApiResponse(
            description="Authentication required."
        ),
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
