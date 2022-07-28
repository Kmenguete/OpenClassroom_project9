from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from litreview.authentication.models import User


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
    return JsonResponse({'status': 200, 'data': payload})


@login_required
def follow_user(request):
    return render(request, 'follow/subscription.html')


@login_required
def unfollow_user(request):
    return render(request, 'follow/subscription.html')
