# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'  # ✅ registers the namespace

urlpatterns = [
    path('', views.home, name='home'),
]
