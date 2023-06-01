from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='users_index'),
    path('create', views.create_new, name='users_create'),
    path('view/<int:user_id>', views.view, name='users_view'),
    path('edit/<int:user_id>', views.edit, name='users_edit'),
    path('delete/<int:user_id>', views.delete, name='users_delete'),
    
    path('register/', views.register, name='register'),
    path('getAllUsers/', views.getAllUsers, name='getAllUsers'),
    path('activate-user/<int:user_id>', views.activateUser, name='activate_user'),
]
