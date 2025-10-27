# vault/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PasswordEntry, Category
from .forms import PasswordEntryForm, CategoryForm
from .utils import decrypt_password
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv
import json
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from .encryption import encrypt_text, decrypt_text

@login_required
def dashboard(request):
    user = request.user
    categories = Category.objects.filter(user=user).annotate(count=Count('entries'))
    entries_qs = PasswordEntry.objects.filter(user=user)
    total = entries_qs.count()
    # weak password heuristic: decrypted length < 8 (simple)
    weak_count = 0
    for e in entries_qs:
        pwd = decrypt_password(e.password_encrypted)
        if len(pwd) < 8:
            weak_count += 1
    tip_list = [
        "Avoid reusing passwords for important accounts.",
        "Use at least 12 characters including numbers & symbols.",
        "Mark frequently used accounts as favorites for quick access."
    ]
    import random
    tip = random.choice(tip_list)
    return render(request, 'vault/dashboard.html', {
        'categories': categories,
        'total': total,
        'weak_count': weak_count,
        'tip': tip,
    })


@login_required
def list_passwords(request):
    q = request.GET.get('q', '')
    cat = request.GET.get('category', '')
    page = request.GET.get('page', 1)

    queryset = PasswordEntry.objects.filter(user=request.user)
    if q:
        queryset = queryset.filter(Q(platform_name__icontains=q) | Q(username__icontains=q))
    if cat:
        queryset = queryset.filter(category__id=cat)

    paginator = Paginator(queryset.order_by('-date_added'), 10)
    page_obj = paginator.get_page(page)

    categories = Category.objects.filter(user=request.user)

    return render(request, 'vault/vault_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'q': q,
        'selected_cat': cat,
    })


@login_required
def add_password(request):
    if request.method == 'POST':
        form = PasswordEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user

            # Get the plaintext password from the form
            plain_password = form.cleaned_data.get('password')

            # Encrypt it before saving
            if plain_password:
                entry.password_encrypted = encrypt_text(plain_password)

            entry.save()
            return redirect('vault:list_passwords')
    else:
        form = PasswordEntryForm()

    return render(request, 'vault/add_password.html', {'form': form})

@login_required
def edit_password(request, pk):
    entry = get_object_or_404(PasswordEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PasswordEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('vault:list_passwords')
    else:
        form = PasswordEntryForm(instance=entry)
    return render(request, 'vault/edit_password.html', {'form': form, 'entry': entry})


@login_required
def detail_password(request, pk):
    entry = get_object_or_404(PasswordEntry, pk=pk, user=request.user)

    # 🔓 Decrypt the stored password
    try:
        decrypted_password = decrypt_text(entry.password_encrypted)
    except Exception:
        decrypted_password = "[Error decrypting password]"

    return render(
        request,
        'vault/vault_detail.html',
        {
            'entry': entry,
            'password_plain': decrypted_password
        }
    )


@login_required
def delete_password(request, pk):
    entry = get_object_or_404(PasswordEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('vault:list_passwords')
    return render(request, 'vault/delete_confirm.html', {'entry': entry})


@login_required
def manage_categories(request):
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user
            cat.save()
            return redirect('vault:manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'vault/categories.html', {'form': form, 'categories': categories})


@login_required
def export_json(request):
    entries = PasswordEntry.objects.filter(user=request.user)
    payload = []
    for e in entries:
        payload.append({
            'platform_name': e.platform_name,
            'username': e.username,
            'password_encrypted': e.password_encrypted,
            'url': e.url,
            'notes': e.notes,
            'category': e.category.name if e.category else None,
            'favorite': e.favorite,
            'date_added': e.date_added.isoformat(),
        })
    response = HttpResponse(json.dumps(payload, indent=2), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=campusvault_backup.json'
    return response


@login_required
def export_csv(request):
    entries = PasswordEntry.objects.filter(user=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=campusvault_backup.csv'
    writer = csv.writer(response)
    writer.writerow(['platform_name', 'username', 'password_encrypted', 'url', 'notes', 'category', 'favorite', 'date_added'])
    for e in entries:
        writer.writerow([e.platform_name, e.username, e.password_encrypted, e.url or '', e.notes or '', e.category.name if e.category else '', e.favorite, e.date_added.isoformat()])
    return response


@login_required
@require_POST
def import_json(request):
    # expects a file upload in 'backup_file'
    f = request.FILES.get('backup_file')
    if not f:
        return redirect('vault:list_passwords')
    data = json.load(f)
    for item in data:
        cat_name = item.get('category')
        cat = None
        if cat_name:
            cat, _ = Category.objects.get_or_create(user=request.user, name=cat_name)
        PasswordEntry.objects.create(
            user=request.user,
            platform_name=item.get('platform_name',''),
            username=item.get('username',''),
            password_encrypted=item.get('password_encrypted',''),
            url=item.get('url',''),
            notes=item.get('notes',''),
            category=cat,
            favorite=item.get('favorite', False)
        )
    return redirect('vault:list_passwords')
