from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from authentication.models import User

from litreview.follow.models import UserFollows


@login_required
def subscriptions(request):
    return render(request, 'follow/subscriptions.html')


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


@login_required
def unfollow_user(request):
    if request.method == 'POST':
        value = request.POST['value']
        user = request.POST['user']
        followed_user = request.POST['followed_user']
        if value == 'unfollow':
            followers_count = UserFollows.objects.delete(user=user, followed_user=followed_user)
            followers_count.save()
