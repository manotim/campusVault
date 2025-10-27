# vault/urls.py
from django.urls import path
from . import views

app_name = 'vault'

urlpatterns = [
   
    path('', views.dashboard, name='dashboard'),
    path('list/', views.list_passwords, name='list_passwords'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-password/', views.add_password, name='add_password'),
    path('edit-password/<int:pk>/', views.edit_password, name='edit_password'),
    path('detail/<int:pk>/', views.detail_password, name='detail_password'),
    path('delete-password/<int:pk>/', views.delete_password, name='delete_password'),
    path('categories/', views.manage_categories, name='manage_categories'),

    # export/import
    path('export/json/', views.export_json, name='export_json'),
    path('export/csv/', views.export_csv, name='export_csv'),
    path('import/json/', views.import_json, name='import_json'),
]
