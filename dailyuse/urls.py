from django.contrib import admin
from django.urls import path, include

api_urlpatterns = [
    path('todos/', include('todos.urls', 'todos')),
    path('users/', include('users.urls', 'users'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns))
]
