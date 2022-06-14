from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'reviews/home.html')


@login_required
def ask_review(request):
    return render(request, 'reviews/ask_review.html')
