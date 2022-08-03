from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from authentication.models import User


@login_required
def subscriptions(request):
    return render(request, 'follow/subscriptions.html')


@login_required
def follower(request):
    pass


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
    pass
