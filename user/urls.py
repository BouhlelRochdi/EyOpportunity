from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    
    path('', views.index, name='users_index'),
    
    # admin
    path('create-admin/', views.createAdmin, name='create_admin'),
    
    # User part
    path('view/<int:user_id>', views.view, name='users_view'),
    
    path('create-user/', views.create_new, name='users_create'),
    path('edit/<int:user_id>', views.edit, name='users_edit'),
    path('register/', views.register, name='register'),
    path('login/', views.sign_in, name='login'),
    
    path('getAllUsers/', views.getAllUsers, name='getAllUsers'),
    path('get-user-by-id/<int:user_id>', views.getUserById, name='get_user_by_id'),
    path('get-user-by-email/<str:email>', views.getUserByEmail, name='get_user_by_email'),
    
    path('get-deactivate-user/', views.getDeactivatedUsers, name='deactivate_user'),
    path('get-activate-user/', views.getActivatedUsers, name='activate_user'),
    path('activate-user/<int:id>', views.activateUser, name='activate_user'),
    
    path('get-users-by-equipe/<int:equipe_id>', views.getUsersBelongingToEquipe, name='get_user_by_equipe'),
    path('delete-user/<int:user_id>', views.deleteUser, name='delete_user'),
    
    #############################
    # archive part
    path('create-archive/', views.createArchive, name='archive_create'),
    path('affect-archive-to-equipe/<int:archive_id>/<int:equipe_id>', views.affectArchiveToEquipe, name='affect_archive_to_equipe'),
    path('get-archives/', views.getFullArchive, name='get_full_archives'),
    path('get-user-archive/<int:user_id>', views.getArchiveByUser, name='get_user_archives'),
    path('update-archive/<int:archive_id>', views.update_archive, name='update_archives'),
    path('archive-by-equipe/<int:equipe_id>', views.getArchiveByEquipe, name='archives_by_equipe'),
    path('delete-archive/<int:archive_id>', views.deleteArchive, name='delete_archive'),
    
    path('getArchiveByEquipe/<int:archive_id>', views.getEquipeByArchive_old, name='get_archive_by_equipe'),
    
    
    path('download-archive/<int:archive_id>', views.downloadArchiveFile, name='download_archive'),
    
    #############################
    # equipe part
    path('create-equipe/', views.createEquipe, name='create_equipe'),
    path('get-all-equipes/', views.getAllEquipes, name='get_all_equipes'),
    path('get-equipe-by-id/<int:equipe_id>', views.getEquipeById, name='get_equipe_by_id'),
    path('get-all-equipes-Users/', views.getAllEquipesAndUsers, name='get_all_equipes'),
    path('get-members-by-equipe/<int:equipe_id>', views.getMembersByEquipe, name='get_members_by_equipe'),
    path('delete-equipe/<int:equipe_id>', views.deleteEquipe, name='delete_equipe'),
    path('update-equipe/<int:equipe_id>', views.updateEquipe, name='update_equipe'),
    
    
    path('affect-archive-to-equipe/<int:archive_id>/<int:equipe_id>', views.affectArchiveToEquipe, name='affect_archive_to_equipe'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)