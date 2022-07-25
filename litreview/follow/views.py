from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from litreview.follow.forms import UserFollowForm


@login_required
def subscriptions(request):
    user_follow_form = UserFollowForm()
    if request.method == 'POST':
        user_follow_form = UserFollowForm(request.POST)
        if user_follow_form.is_valid():
            return redirect('home')
    context = {'user_follow_form': user_follow_form}
    return render(request, 'follow/subscriptions.html', context=context)
