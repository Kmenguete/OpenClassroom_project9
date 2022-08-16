from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, user_logged_out
from django.conf import settings
from authentication.models import User
from django.views.generic import View

from . import forms


def signup_page(request):
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have successfully signed up!")
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            print(form.errors)
            messages.error(request, "The sign up form is not valid.")
            return redirect("signup")
    return render(request, "authentication/signup.html", context={"form": form})


def user_delete(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        user.delete()
        return redirect(settings.DELETE_REDIRECT_URL)
    return render(request, "authentication/user_delete.html", {"user": user})


class LoginPageView(View):
    template_name = "authentication/login.html"
    login_form = forms.LoginForm

    def get(self, request):
        form = self.login_form()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = self.login_form(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Happy to see you again {user.username}!")
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(request, "Invalid username or password !")
                return redirect("login")
        return render(request, self.template_name, context={"form": form})


def show_message(request, **kwargs):
    messages.success(request, "You successfully logged out.")


user_logged_out.connect(show_message)
