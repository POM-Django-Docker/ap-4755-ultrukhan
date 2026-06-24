from django.urls import path
from . import views

urlpatterns = [
    path('', views.author_list_view, name='author_list'),
    path('create/', views.author_create_view, name='author_create'),
    path('<int:author_id>/delete/', views.author_delete_view, name='author_delete'),
]