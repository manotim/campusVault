# vault/forms.py
from django import forms
from .models import PasswordEntry, Category
from .utils import encrypt_password, decrypt_password

class PasswordEntryForm(forms.ModelForm):
    password_plain = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(render_value=False, attrs={'class': 'border rounded p-2 w-full', 'autocomplete': 'new-password'}),
        required=True
    )

    class Meta:
        model = PasswordEntry
        fields = ['platform_name', 'username', 'password_plain', 'url', 'notes', 'category', 'favorite']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)
        # If editing existing instance, fill password_plain with decrypted value
        if instance and instance.password_encrypted:
            try:
                self.fields['password_plain'].initial = decrypt_password(instance.password_encrypted)
            except Exception:
                self.fields['password_plain'].initial = ''

    def save(self, commit=True):
        obj = super(forms.ModelForm, self).save(commit=False)
        plain = self.cleaned_data.get('password_plain', '')
        obj.password_encrypted = encrypt_password(plain)
        if commit:
            obj.save()
        return obj


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'})
        }
