from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from . import forms
from ..authentication.models import User


@login_required
def subscriptions(request):
    return render(request, 'follow/subscription.html')


@login_required
def search_users(request):
    users = User.objects.all()
    search_form = forms.SearchForm()
    if request.moethod == 'POST':
        pass
    context = {'search_form': search_form, 'users': users}
    return render(request, 'follow/subscription.html', context=context)


@login_required
def follow_user(request):
    return render(request, 'follow/subscription.html')


@login_required
def unfollow_user(request):
    return render(request, 'follow/subscription.html')
