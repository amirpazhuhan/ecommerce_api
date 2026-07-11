from django.urls import path
from .views import MeView, RegisterView
from .views import(
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token-refresh'),
    path('me/', MeView.as_view(), name='me'),

]
