from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from . import forms
from . import models
from .forms import ReviewNewBookForm
from ..authentication.models import User


@login_required
def home(request):
    reviews = models.Review.objects.all()
    tickets = models.Ticket.objects.all()
    return render(request, 'reviews/home.html', context={'tickets': tickets, 'reviews': reviews})


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


@login_required
def create_review(request):
    create_review_form = forms.CreateReviewForm()
    if request.method == 'POST':
        create_review_form = forms.CreateReviewForm(request.POST, files=request.FILES)
        if create_review_form.is_valid():
            review = create_review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('home')
    context = {'create_review_form': create_review_form}
    return render(request, 'reviews/create_review.html', context=context)


@login_required
class CreateNewReviewView(UpdateView):
    model = User
    form_class = ReviewNewBookForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(CreateNewReviewView, self).get_form_kwargs()
        kwargs.update(instance={
            'ask_review': self.object,
            'create_new_review': self.object.create_new_review,
        })
        return kwargs
