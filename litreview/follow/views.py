from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from authentication.models import User

from . import models


@login_required
def subscriptions(request):
    follows = models.UserFollows.objects.filter(user=request.user)
    followers = models.UserFollows.objects.filter(followed_user__contains=request.user)
    return render(request, 'follow/subscriptions.html', context={'follows': follows, 'followers': followers})


@login_required
def follower(request):
    # search_bar = search_users(request)
    if request.method == 'POST':
        username = request.POST['username']
        if username is not None:
            user = User.objects.get(username=username)
            user_follows = models.UserFollows.objects.create(user=request.user, followed_user=user)
            user_follows.save()
            return redirect('subscriptions')
        else:
            messages.error(request, "The user you are looking for does not exist.")
        return render(request, 'follow/subscriptions.html')
    return render(request, 'follow/subscriptions.html')


"""@login_required
def search_users(request):
    username = request.GET.get('username')
    payload = []
    if username:
        users = User.objects.filter(username__icontains=username)
        for user in users:
            payload.append(user.username)
    return JsonResponse({'status': 200, 'data': payload})"""


def unfollow_user(request):
    return render(request, 'follow/subscriptions.html')
