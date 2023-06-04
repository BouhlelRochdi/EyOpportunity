from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.index, name='users_index'),
    
    # admin
    path('create-admin/', views.createAdmin, name='create_admin'),
    
    # User part
    path('create', views.create_new, name='users_create'),
    path('view/<int:user_id>', views.view, name='users_view'),
    path('edit/<int:user_id>', views.edit, name='users_edit'),
    
    path('register/', views.register, name='register'),
    path('login/', views.sign_in, name='login'),
    path('getAllUsers/', views.getAllUsers, name='getAllUsers'),
    path('activate-user/<int:id>', views.activateUser, name='activate_user'),
    path('get-deactivate-user/', views.getDeactivatedUsers, name='deactivate_user'),
    path('get-activate-user/', views.getActivatedUsers, name='activate_user'),
    path('delete-user/<int:user_id>', views.deleteUser, name='delete_user'),
    
    #############################
    # archive part
    path('create-archive/<int:user_id>/<int:equipe_id>', views.createArchive, name='archive_create'),
    path('get-archives/', views.getFullArchive, name='get_full_archives'),
    path('get-user-archive/<int:user_id>', views.getArchiveByUser, name='get_user_archives'),
    path('update-archive/<int:archive_id>', views.update_archive, name='update_archives'),
    path('archive-by-equipe/<int:equipe_id>', views.getArchiveByEquipe, name='archives_by_equipe'),
    
    #############################
    # equipe part
    path('create-equipe/', views.createEquipe, name='create_equipe'),
    path('get-all-equipes/', views.getAllEquipes, name='get_all_equipes'),
    path('get-equipe-by-id/<int:equipe_id>', views.getEquipeById, name='get_equipe_by_id'),
    path('get-all-equipes-Users/', views.getAllEquipesAndUsers, name='get_all_equipes'),
    path('get-members-by-equipe/<int:equipe_id>', views.getMembersByEquipe, name='get_members_by_equipe'),
    
    
    
]
