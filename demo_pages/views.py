from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from minddistrict_connect.controller import DLO


def login_view(request):
    """View for handling user login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile_dashboard')  # Redirect to profile dashboard after login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect(f'{settings.LOGIN_URL}')


@login_required
def profile_dashboard(request):
    """View to display user profile dashboard"""
    user = request.user

    try:
        dlo = DLO(user)
        resources = dlo.get_resources()
    except ValueError as err:
        messages.error(request, str(err))
        resources = {}

    context = {
        'user': user,
        'data': resources,
        'profile': user.platformprofile

    }
    return render(request, 'profile_dashboard.html', context)
