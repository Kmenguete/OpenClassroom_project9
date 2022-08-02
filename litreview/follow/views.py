from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from authentication.models import User

from .models import UserFollows


@login_required
def subscriptions(request):
    return render(request, 'follow/subscriptions.html')


@login_required
def follower(request):
    users = UserFollows.user
    followed_users = UserFollows.followed_user
    if search_users(request=request) is not None:
        user = request.GET.get('user')
        if user is not None:
            user.save()
        else:
            messages.error(request, "The user you are looking for does not exist.")
    context = {'users': users, 'followed_users': followed_users}
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


@login_required
def follow_user(request):
    if request.method == 'POST':
        value = request.POST['value']
        user = request.POST['user']
        followed_user = request.POST['followed_user']
        if value == 'follow':
            followers_count = UserFollows.objects.create(user=user, followed_user=followed_user)
            followers_count.save()
        return redirect('follow_user/?user=' + user)


@login_required
def unfollow_user(request):
    if request.method == 'POST':
        value = request.POST['value']
        user = request.POST['user']
        followed_user = request.POST['followed_user']
        if value == 'unfollow':
            followers_count = UserFollows.objects.delete(user=user, followed_user=followed_user)
            followers_count.save()
        return redirect('unfollow_user/?user=' + user)
