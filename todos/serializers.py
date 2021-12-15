from rest_framework.serializers import ModelSerializer, CharField
from todos.models import Todo
from users.models import User

class TodoSerializer(ModelSerializer):
  class Meta:
    model = Todo
    fields = ('id', 'title', 'description', 'created_at', 'updated_at', 'user')
    # read_only_fields = ['id', 'created_at', 'updated_at']
