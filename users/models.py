from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


# Create your models here.
class User(AbstractUser):
  email = models.EmailField(unique=True)
  password = models.CharField(max_length=128)
  username = None
  name = models.CharField(max_length=128)
  is_email_verified = models.BooleanField(null=True)
  mobile = models.CharField(max_length=13, validators=[RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Enter a valid mobile number")], default='+911234567890')

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['mobile']
