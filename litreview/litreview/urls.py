"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import authentication.views
import reviews.views
import follow.views
from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", authentication.views.LoginPageView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "change-password/",
        PasswordChangeView.as_view(
            template_name="authentication/password_change_form.html"
        ),
        name="password_change",
    ),
    path(
        "change-password-done/",
        PasswordChangeDoneView.as_view(
            template_name="authentication/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("home/", reviews.views.home, name="home"),
    path("posts/", reviews.views.posts, name="posts"),
    path("update_review/<int:id>/", reviews.views.update_review, name="update_review"),
    path("update_ticket/<int:id>/", reviews.views.update_ticket, name="update_ticket"),
    path("signup/", authentication.views.signup_page, name="signup"),
    path(
        "delete_account/<int:id>/delete/",
        authentication.views.user_delete,
        name="delete_account",
    ),
    path("ask_review/", reviews.views.ask_review, name="ask_review"),
    path("create_review/<int:id>/", reviews.views.create_review, name="create_review"),
    path(
        "create_new_review/", reviews.views.create_new_review, name="create_new_review"
    ),
    path("subscriptions/", follow.views.subscriptions, name="subscriptions"),
    path("search/", follow.views.search_users, name="search_users"),
    path("follower/", follow.views.follower, name="follower"),
    path("unfollow_user/<int:id>/", follow.views.unfollow_user, name="unfollow_user"),
    path("delete_ticket/<int:id>/delete/",
         reviews.views.delete_ticket,
         name="delete_ticket"),
    path("delete_review/<int:id>/delete/",
         reviews.views.delete_review,
         name="delete_review"),
    path("delete_new_review/<int:id>/delete/",
         reviews.views.delete_new_review,
         name="delete_new_review"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
