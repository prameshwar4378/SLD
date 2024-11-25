from django.urls import path
from .views import *

urlpatterns = [
    path('login-token', CustomAuthToken.as_view(), name='api_token_auth'),
]