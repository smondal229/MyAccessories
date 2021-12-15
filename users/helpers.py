import jwt
from django.utils import timezone
from django.conf import settings

def token_for(user):
  access_token_time = timezone.now() + timezone.timedelta(days=1)
  refresh_token_time = timezone.now() + timezone.timedelta(days=30)

  access_token = jwt.encode({ 'exp': access_token_time, 'id': user.pk }, key=settings.SECRET_KEY, algorithm="HS256")
  refresh_token = jwt.encode({ 'exp': refresh_token_time, 'id': user.pk }, key=settings.SECRET_KEY, algorithm="HS256")

  return { 'access_token': access_token, 'refresh_token': refresh_token }
