from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.conf import settings
from authentication.models import User
from django.contrib.auth.views import LoginView, LogoutView

from . import forms


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have successfully signed up!")
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(request, "The sign up form is incomplete.")
            return redirect('signup')
    return render(request, 'authentication/signup.html', context={'form': form})


def user_delete(request, id):
    user = User.objects.get(id=id)
    if request.method == 'POST':
        user.delete()
        return redirect(settings.DELETE_REDIRECT_URL)
    return render(request, 'authentication/user_delete.html', {'user': user})


class MyLoginView(LoginView):
    template_name = 'authentication/login.html'

    def form_valid(self, form):
        user = form.get_user()
        messages.success(self.request, f'Happy to see you {user.username}')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'incorrect username or password.')
        return super().form_invalid(self)


class MyLogoutView(LogoutView):

    def form_valid(self):
        return messages.success(self.request, 'You successfully logged out.')
