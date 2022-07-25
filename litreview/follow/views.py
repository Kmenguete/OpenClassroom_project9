from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . import forms


@login_required
def subscriptions(request):
    user_follow_form = forms.UserFollowForm()
    if request.method == 'POST':
        user_follow_form = forms.UserFollowForm(request.POST)
        if user_follow_form.is_valid():
            return redirect('home')
    context = {'user_follow_form': user_follow_form}
    return render(request, 'follow/subscriptions.html', context=context)
