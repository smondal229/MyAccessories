import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework import status
from .serializers import UserSerializer
from .models import User
from .services import user_verification_mail
from .helpers import token_for
from .backends import JWTAuthentication


@api_view(['POST'])
@authentication_classes(())
def register(request):
  serialized_data = UserSerializer(data=request.data)
  serialized_data.is_valid(raise_exception=True)
  serialized_data.save()
  user_verification_mail(user=serialized_data.data)
  return Response(serialized_data.data)

@api_view(['POST'])
@authentication_classes(())
def verify_email(request, verify_token):
  try:
    data = jwt.decode(verify_token, key=settings.EMAIL_VERIFICATION_SECRET, algorithms=['HS256'])
    user = User.objects.get(email=data['user']['email'])
    if user is not None and user.is_email_verified is False:
      user.is_email_verified = True
      user.save(update_fields=['is_email_verified'])
      return Response(status=status.HTTP_200_OK, data={'message': 'Successfully verified'})
    if user.is_email_verified:
      return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'User email is already verified'})

    return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Invalid User'})
  except jwt.exceptions.ExpiredSignatureError as exc:
    return Response(status=status.HTTP_400_BAD_REQUEST, data={ 'message': str(exc) })


@api_view(['POST'])
@authentication_classes(())
def login(request):
  email = request.data['email']
  password = request.data['password']

  user = User.objects.get(email=email)

  if user.is_email_verified is False:
    raise AuthenticationFailed('User email is not verified!')

  if user is None:
    raise AuthenticationFailed('User not found!')

  if not user.check_password(password):
    raise AuthenticationFailed('Incorrect password!')

  token_data =  token_for(user)
  serialized_user_data = UserSerializer(user)

  return Response(status=status.HTTP_200_OK, data={ **token_data, 'user': serialized_user_data.data })

def retry_email_verification(request, email):
  user = User.objects.get(email=email)

  if user is None:
    return NotFound(detail="User email not found")

  user_verification_mail(user=user)

  return Response(status=status.HTTP_200_OK, data={ 'message': 'Verification mail sent successfully' })


@api_view(['POST'])
@authentication_classes(())
def refresh_token(request, token):
  try:
    payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
  except jwt.exceptions.ExpiredSignatureError as exc:
    return Response(status=status.HTTP_400_BAD_REQUEST, data={ 'message': str(exc) })

  access_token_time = timezone.now() + timezone.timedelta(days=1)
  access_token = jwt.encode({ 'exp': access_token_time, 'id': payload['id'] }, key=settings.SECRET_KEY, algorithm="HS256")
  return Response(status=status.HTTP_200_OK, data={ 'access_token': access_token })
