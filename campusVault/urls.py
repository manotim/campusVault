# campusVault/urls.py
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

# campusVault/urls.py

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts app
    path('accounts/', include('accounts.urls')),

    # Dashboard app
    path('', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),

    # Vault app
    path('vault/', include(('vault.urls', 'vault'), namespace='vault')),
]

