from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from todos.models import Todo
from todos.serializers import TodoSerializer
from .models import Todo


@api_view(['GET'])
def index(request):
  user = request.user
  paginator = PageNumberPagination()
  per_page_param = request.GET.get('per_page')
  paginator.page_size = settings.DEFAULT_PAGE_SIZE if per_page_param is None else per_page_param
  todos_list = Todo.objects.filter(user=user)
  context = paginator.paginate_queryset(todos_list, request)
  serialized_todos = TodoSerializer(context, many = True)

  return paginator.get_paginated_response(serialized_todos.data)


@api_view(['GET'])
def get(request, todo_id):
  try:
    serialized_todos = TodoSerializer(Todo.objects.get(id=todo_id))
    return Response(status=status.HTTP_200_OK, data=serialized_todos.data)
  except ObjectDoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create(request):
  todo_data = request.data.copy()
  todo_data['user'] = request.user.pk

  todo = TodoSerializer(data=todo_data)
  todo.is_valid(raise_exception=True)
  todo.save()
  return Response(status=status.HTTP_200_OK, data=todo.data)
