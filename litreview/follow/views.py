from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from authentication.models import User

from . import models


@login_required
def subscriptions(request):
    return render(request, 'follow/subscriptions.html')


@login_required
def follower(request):
    user_follower = models.UserFollows.objects.filter().values('user')
    followed_user = models.UserFollows.objects.filter().values('followed_user')
    search_bar = search_users(request)
    if search_bar is not None:
        username = request.POST['username']
        user_to_follow = User.objects.get(username=username)
        if user_to_follow is not None:
            user_follows = models.UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
            user_follows.save()
            return redirect('subscriptions')
        else:
            messages.error(request, "The user you are looking for does not exist.")

    context = {'user_follower': user_follower, 'followed_user': followed_user}
    return render(request, 'follow/subscriptions.html', context=context)


@login_required
def search_users(request):
    username = request.GET.get('username')
    payload = []
    if username:
        users = User.objects.filter(username__icontains=username)
        for user in users:
            payload.append(user.username)
    return JsonResponse({'status': 200, 'data': payload})


def unfollow_user(request):
    return render(request, 'follow/subscriptions.html')
