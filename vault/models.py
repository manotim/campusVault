# vault/models.py
from django.db import models
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']

    def __str__(self):
        return self.name


class PasswordEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_entries')
    platform_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password_encrypted = models.TextField(help_text="Fernet-encrypted token (base64 str)")
    url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='entries')
    favorite = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.platform_name} ({self.username})"

    def get_absolute_url(self):
        return reverse('vault:edit_password', args=[self.pk])
