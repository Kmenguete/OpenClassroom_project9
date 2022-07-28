from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from . import forms


@login_required
def subscriptions(request):
    return render(request, 'follow/subscription.html')


@login_required
def search_users(request):
    search_form = forms.SearchForm()
    if request.moethod == 'POST':
        pass
    context = {'search_form': search_form}
    return render(request, 'follow/subscription.html', context=context)


@login_required
def follow_user(request):
    return render(request, 'follow/subscription.html')


@login_required
def unfollow_user(request):
    return render(request, 'follow/subscription.html')
