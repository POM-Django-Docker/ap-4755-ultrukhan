from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from authentication.models import CustomUser
from order.models import Order
from .forms import RegisterForm, LoginForm


def is_librarian(user):
    return user.is_authenticated and user.role == 1


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            middle_name = form.cleaned_data['middle_name']
            last_name = form.cleaned_data['last_name']
            role = int(form.cleaned_data['role'])

            new_user = CustomUser.create(email, password, first_name, middle_name, last_name)
            if new_user is None:
                form.add_error('email', 'Email already exists')
            else:
                new_user.update(role=role, is_active=True)
                return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'authentication/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = CustomUser.get_by_email(email)
            if user and user.password == password:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect('book_list')
            elif user is None:
                form.add_error('email', 'User not found')
            else:
                form.add_error('password', 'Password is not correct')
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def user_list(request):
    if not is_librarian(request.user):
        return HttpResponseForbidden("Access denied")
    users = CustomUser.objects.all()
    return render(request, 'authentication/user_list.html', {'users': users})


@login_required
def user_detail(request, user_id):
    if not is_librarian(request.user):
        return HttpResponseForbidden("Access denied")
    viewed_user = get_object_or_404(CustomUser, id=user_id)
    orders = Order.objects.filter(user=viewed_user)
    return render(request, 'authentication/user_detail.html', {
        'viewed_user': viewed_user,
        'orders': orders,
    })