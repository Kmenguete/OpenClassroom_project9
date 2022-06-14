from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from . import forms


@login_required
def home(request):
    return render(request, 'reviews/home.html')


@login_required
def ask_review(request):
    ask_review_form = forms.AskReviewForm()
    if request.method == 'POST':
        ask_review_form = forms.AskReviewForm(request.POST)
        if ask_review_form.is_valid():
            ask_review_form.save()
            return redirect('home')
    context = {'ask_review_form': ask_review_form}
    return render(request, 'reviews/ask_review.html', context=context)
