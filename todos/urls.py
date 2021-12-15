from django.urls import path
from todos.views import index, get, create

app_name = 'Todos'

urlpatterns = [
  path('', index, name="index"),
  path('get/<todo_id>/', get, name="get"),
  path('create/', create, name="create")
]
