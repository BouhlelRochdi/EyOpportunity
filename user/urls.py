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
    path('login/', views.sign_in, name='login'),
    path('getAllUsers/', views.getAllUsers, name='getAllUsers'),
    path('activate-user/<int:id>', views.activateUser, name='activate_user'),
    
    #############################
    # archive part
    path('create-archive/<int:user_id>/<int:equipe_id>', views.createArchive, name='archive_create'),
    path('get-archives/', views.getFullArchive, name='get_full_archives'),
    path('get-user-archive/<int:user_id>', views.getArchiveByUser, name='get_user_archives'),
    path('update-archive/<int:user_id>', views.getArchiveByUser, name='update_archives'),
    
    #############################
    # equipe part
    path('create-equipe/', views.createEquipe, name='create_equipe'),
    path('get-all-equipes/', views.getAllEquipes, name='get_all_equipes'),
    
    
    
    
    
]
