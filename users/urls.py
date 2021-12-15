from django.urls import path
from .views import register, login, verify_email, refresh_token

app_name = "Users"

urlpatterns = [
  path('register/', register, name="register"),
  path('login/', login, name="login"),
  path('verify/<str:verify_token>/', verify_email, name="verify"),
  path('refreshtoken/<str:token>/', refresh_token, name="refresh-token")
]
