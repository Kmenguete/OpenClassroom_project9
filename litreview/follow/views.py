from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import utils
from django.http import JsonResponse
from django.shortcuts import render, redirect

from authentication.models import User

from . import models


@login_required
def subscriptions(request):
    follows = models.UserFollows.objects.filter(user=request.user)
    followers = models.UserFollows.objects.filter(
        followed_user__username__contains=request.user.username
    )
    return render(
        request,
        "follow/subscriptions.html",
        context={"follows": follows, "followers": followers},
    )


@login_required
def follower(request):
    # search_bar = search_users(request)
    if request.method == "POST":
        username = request.POST["username"]
        if username is not None:
            try:
                user = User.objects.get(username=username)
                if user == request.user:
                    messages.error(request, "You cannot follow yourself.")
                    return redirect("subscriptions")
                else:
                    user_follows = models.UserFollows.objects.create(
                        user=request.user, followed_user=user
                    )
                    user_follows.save()
                    messages.success(request, "You follow " + str(username) + ".")
                    return redirect("subscriptions")
            except User.DoesNotExist:
                messages.error(request, "The user you are looking for does not exist.")
                return redirect("subscriptions")
            except utils.IntegrityError:
                messages.error(request, "You already follow " + str(username) + ".")
                return redirect("subscriptions")
    return render(request, "follow/subscriptions.html")


@login_required
def search_users(request):
    username = request.GET.get("username")
    payload = []
    if username:
        users = User.objects.filter(username__icontains=username)
        for user in users:
            payload.append(user.username)
    return JsonResponse({"status": 200, "data": payload})


def unfollow_user(request, id):
    user = request.user
    followed_user = User.objects.get(id=id)
    user_follows = models.UserFollows.objects.get(
        user=user, followed_user=followed_user
    )
    if request.method == "GET":
        user_follows.delete()
        return redirect("subscriptions")
    return render(
        request, "follow/subscriptions.html", context={"user_follows": user_follows}
    )
