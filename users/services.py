from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
import jwt

def user_verification_mail(user):
  verification_token = jwt.encode({ 'user': user, 'exp': timezone.now() + timezone.timedelta(minutes=5) }, key=settings.EMAIL_VERIFICATION_SECRET, algorithm="HS256")
  subject = "Verify Email"
  name = user['name']
  txt_message = render_to_string('emails/signup/signup.txt')
  html_message = render_to_string('emails/signup/signup.html', { 'name': name, 'token': verification_token })

  send_mail(subject=subject, message=txt_message, from_email=settings.EMAIL_HOST_USER, html_message=html_message, recipient_list=[user['email']], fail_silently=False)
