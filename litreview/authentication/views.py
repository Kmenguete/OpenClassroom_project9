from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from . import forms


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Hello, {user.username}! You are logged in.'
            else:
                message = 'Incorrect username.'
    return render(request, 'authentication/login.html', context={'form': form, 'message': message})


def logout_user(request):

    logout(request)
    return redirect('login')
