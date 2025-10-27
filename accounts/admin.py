from django.contrib import admin
from .models import Category, PasswordEntry


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')


@admin.register(PasswordEntry)
class PasswordEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'username', 'date_created')
    search_fields = ('title', 'username', 'category__name')
    list_filter = ('category', 'date_created')
