from django.db import models
from users.models import User

class Todo(models.Model):
  title = models.CharField(null=False, blank=False, max_length=100)
  description = models.TextField(max_length=500)
  user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title

  class Meta:
    indexes = [
      models.Index(fields=['created_at']),
      models.Index(fields=['updated_at'])
    ]
