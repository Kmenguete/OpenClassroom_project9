from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from . import forms
from ..authentication.models import User


@login_required
def subscriptions(request):
    return render(request, 'follow/subscription.html')


@login_required
def search_users(request):
    user = request.GET.get('user')
    payload = []
    if user:
        users = User.objects.filter(name__contain=user.username)
        for user in users:
            payload.append(user.username)
    """
    search_form = forms.SearchForm()
    if request.method == 'POST':
        pass
    context = {'search_form': search_form, 'user': user}
    return render(request, 'follow/subscription.html', context=context)
    """


@login_required
def follow_user(request):
    return render(request, 'follow/subscription.html')


@login_required
def unfollow_user(request):
    return render(request, 'follow/subscription.html')
