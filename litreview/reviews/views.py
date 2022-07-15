from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from .forms import AskReviewForm, CreateNewReviewForm
from .models import Ticket


@login_required
def home(request):
    reviews = models.Review.objects.all()
    ticket_of_reviews = models.Review.objects.filter().values('ticket')
    real_tickets = exclude_tickets_of_reviews(ticket_of_reviews)

    return render(request, 'reviews/home.html', context={'real_tickets': real_tickets, 'reviews': reviews})


def exclude_tickets_of_reviews(ticket_of_reviews):
    tickets_to_excludes = [ticket_of_reviews]
    for ticket in tickets_to_excludes:
        tickets = models.Ticket.objects.exclude(id__in=ticket)
        return tickets


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
    ticket = get_ticket()
    create_review_form = forms.CreateReviewForm()
    if request.method == 'POST':
        create_review_form = forms.CreateReviewForm(request.POST)
        if create_review_form.is_valid():
            review = create_review_form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('home')

    context = {'create_review_form': create_review_form, 'ticket': ticket}
    return render(request, 'reviews/create_review.html', context=context)


def get_ticket():
    ticket_of_reviews = models.Review.objects.filter().values('ticket')
    real_tickets = exclude_tickets_of_reviews(ticket_of_reviews)
    for ticket in real_tickets:
        real_ticket = models.Ticket.objects.get(id=ticket.id)
        return real_ticket


@login_required
def create_new_review(request: WSGIRequest):
    form_ask = AskReviewForm(prefix="ask")
    form_create = CreateNewReviewForm(prefix="create")
    create_new_review_form = form_ask, form_create
    if request.method == 'POST':
        form_ask = AskReviewForm(request.POST, files=request.FILES, prefix="ask")
        form_create = CreateNewReviewForm(request.POST, prefix="create")
        if form_ask.is_valid() and form_create.is_valid():
            ticket = form_ask.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = form_create.save(commit=False)
            review.user = request.user
            review.ticket = Ticket.objects.get(pk=ticket.pk)
            review.save()

            return redirect('home')

    return render(request, 'reviews/create_new_review.html', context={'create_new_review_form': create_new_review_form})
