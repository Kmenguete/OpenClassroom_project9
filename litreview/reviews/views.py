from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from . import forms
from . import models


@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    return render(request, 'reviews/home.html', context={'tickets': tickets})


@login_required
def ask_review(request):
    ask_review_form = forms.AskReviewForm()
    if request.method == 'POST':
        ask_review_form = forms.AskReviewForm(request.POST, files=request.FILES)
        if ask_review_form.is_valid():
            ticket = ask_review_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    context = {'ask_review_form': ask_review_form}
    return render(request, 'reviews/ask_review.html', context=context)
