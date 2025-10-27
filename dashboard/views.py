# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from vault.models import PasswordEntry, Category
from django.db.models import Count

@login_required
def home(request):
    total = PasswordEntry.objects.filter(user=request.user).count()
    per_category = Category.objects.filter(user=request.user).annotate(count=Count('entries'))
    # weak password heuristic: entries with short decrypted password (we'll skip decryption cost here)
    # For now show last login from request.user.last_login
    last_login = request.user.last_login
    tips = [
        "Do not reuse passwords across important accounts.",
        "Use at least 12 characters with numbers and symbols.",
        "Mark frequently used accounts as favorites."
    ]
    import random
    tip = random.choice(tips)
    return render(request, 'dashboard/home.html', {'total': total, 'per_category': per_category, 'last_login': last_login, 'tip': tip})
