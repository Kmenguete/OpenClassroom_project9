from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def subscriptions(request):
    return render(request, 'follow/subscription.html')


@login_required
def search_users(request):
    return render(request, 'follow/subscription.html')


@login_required
def follow_user(request):
    return render(request, 'follow/subscription.html')


@login_required
def unfollow_user(request):
    return render(request, 'follow/subscription.html')
