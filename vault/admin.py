# vault/admin.py
from django.contrib import admin
from .models import Category, PasswordEntry

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')

@admin.register(PasswordEntry)
class PasswordEntryAdmin(admin.ModelAdmin):
    list_display = ('platform_name', 'username', 'user', 'category', 'date_added')
    search_fields = ('platform_name', 'username', 'user__username')
