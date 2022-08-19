from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from .forms import AskReviewForm, CreateNewReviewForm
from .models import Ticket
from itertools import chain
from follow.models import UserFollows
from django.core.paginator import Paginator


@login_required
def home(request):
    followed_user = UserFollows.objects.filter(user=request.user).values(
        "followed_user"
    )
    reviews_of_followed_user = models.Review.objects.filter(user__in=followed_user)
    ticket_of_reviews_of_followed_user = models.Review.objects.filter(
        user__in=followed_user
    ).values("ticket")
    real_tickets_of_followed_user = exclude_followed_users_tickets_of_reviews(
        followed_user, ticket_of_reviews_of_followed_user
    )
    tickets_and_reviews_of_followed_user = list(
        chain(reviews_of_followed_user, real_tickets_of_followed_user)
    )
    reviews_of_user = models.Review.objects.filter(user=request.user)
    tickets_and_reviews_of_user = get_posts_of_logged_in_user(request)
    reviews = list(chain(reviews_of_followed_user, reviews_of_user))
    ticket_of_reviews = models.Review.objects.filter(user=request.user).values("ticket")
    real_tickets_of_user = exclude_users_tickets_of_reviews(request, ticket_of_reviews)
    real_tickets = list(chain(real_tickets_of_followed_user, real_tickets_of_user))
    tickets_and_reviews = sorted(
        chain(tickets_and_reviews_of_user, tickets_and_reviews_of_followed_user),
        key=lambda instance: instance.time_created,
        reverse=True,
    )

    paginator = Paginator(tickets_and_reviews, 8)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(
        request,
        "reviews/home.html",
        context={
            "page_object": page_object,
            "reviews": reviews,
            "real_tickets": real_tickets,
        },
    )


def get_posts_of_logged_in_user(request):
    reviews = models.Review.objects.filter(user=request.user)
    ticket_of_reviews = models.Review.objects.filter(user=request.user).values("ticket")
    real_tickets = exclude_users_tickets_of_reviews(request, ticket_of_reviews)
    tickets_and_reviews = sorted(
        chain(reviews, real_tickets),
        key=lambda instance: instance.time_created,
        reverse=True,
    )
    return tickets_and_reviews


def exclude_tickets_of_reviews(ticket_of_reviews):
    tickets_to_excludes = [ticket_of_reviews]
    for ticket in tickets_to_excludes:
        tickets = models.Ticket.objects.exclude(id__in=ticket)
        return tickets


@login_required
def posts(request):
    reviews = models.Review.objects.filter(user=request.user)
    ticket_of_reviews = models.Review.objects.filter(user=request.user).values("ticket")
    real_tickets = exclude_users_tickets_of_reviews(request, ticket_of_reviews)
    tickets_and_reviews = sorted(
        chain(reviews, real_tickets),
        key=lambda instance: instance.time_created,
        reverse=True,
    )

    paginator = Paginator(tickets_and_reviews, 8)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(
        request,
        "reviews/posts.html",
        context={
            "page_object": page_object,
            "reviews": reviews,
            "real_tickets": real_tickets,
        },
    )


def exclude_users_tickets_of_reviews(request, ticket_of_reviews):
    tickets_to_excludes = [ticket_of_reviews]
    for ticket in tickets_to_excludes:
        tickets = models.Ticket.objects.filter(user=request.user).exclude(id__in=ticket)
        return tickets


def exclude_followed_users_tickets_of_reviews(followed_user, ticket_of_reviews):
    tickets_to_excludes = [ticket_of_reviews]
    for ticket in tickets_to_excludes:
        tickets = models.Ticket.objects.filter(user__in=followed_user).exclude(
            id__in=ticket
        )
        return tickets


@login_required
def ask_review(request):
    ask_review_form = forms.AskReviewForm()
    if request.method == "POST":
        ask_review_form = forms.AskReviewForm(request.POST, files=request.FILES)
        if ask_review_form.is_valid():
            ticket = ask_review_form.save(commit=False)
            ticket.user = request.user
            ticket.is_already_replied = False
            ticket.save()
            messages.success(request, "The ticket has been submitted successfully.")
            return redirect("home")
        else:
            messages.error(request, "The ticket is not valid.")
            return redirect("ask_review")
    context = {"ask_review_form": ask_review_form}
    return render(request, "reviews/ask_review.html", context=context)


@login_required
def create_review(request, id):
    ticket = models.Ticket.objects.get(id=id)
    create_review_form = forms.CreateReviewForm()
    create_review_form.ticket = AskReviewForm(instance=ticket)
    if request.method == "POST":
        create_review_form = forms.CreateReviewForm(request.POST)
        if create_review_form.is_valid():
            review = create_review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.ticket.is_already_replied = True
            review.save()
            print(review.ticket.is_already_replied)
            messages.success(request, "The review has been created successfully.")
            return redirect("home")
        else:
            messages.error(request, "The review is not valid.")
            return redirect("create_review", ticket.id)
    context = {"create_review_form": create_review_form, "ticket": ticket}
    return render(request, "reviews/create_review.html", context=context)


@login_required
def create_new_review(request: WSGIRequest):
    form_ask = AskReviewForm(prefix="ask")
    form_create = CreateNewReviewForm(prefix="create")
    create_new_review_form = form_ask, form_create
    if request.method == "POST":
        form_ask = AskReviewForm(request.POST, files=request.FILES, prefix="ask")
        form_create = CreateNewReviewForm(request.POST, prefix="create")
        if form_ask.is_valid() and form_create.is_valid():
            ticket = form_ask.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = form_create.save(commit=False)
            review.user = request.user
            review.ticket = Ticket.objects.get(pk=ticket.pk)
            review.ticket.is_already_replied = True
            review.save()
            messages.success(request, "The review has been created successfully.")
            return redirect("home")
        else:
            messages.error(request, "The review is not valid.")
            return redirect("create_new_review")

    return render(
        request,
        "reviews/create_new_review.html",
        context={"create_new_review_form": create_new_review_form},
    )


@login_required
def update_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.method == "POST":
        ask_review_form = forms.AskReviewForm(
            request.POST, files=request.FILES, instance=ticket
        )
        if ask_review_form.is_valid():
            ask_review_form.save()
            messages.success(request, "The ticket has been successfully updated.")
            return redirect("posts")
        else:
            messages.error(request, "The ticket is not valid.")
            return redirect("update_ticket", ticket.id)
    context = {"ticket": ticket}
    return render(request, "reviews/update_ticket.html", context=context)


@login_required
def update_review(request, id):
    review = models.Review.objects.get(id=id)
    if request.method == "POST":
        create_review_form = forms.CreateReviewForm(request.POST, instance=review)
        if create_review_form.is_valid():
            create_review_form.save()
            messages.success(request, "The review has been successfully updated.")
            return redirect("posts")
        else:
            messages.error(request, "The review is not valid.")
            return redirect("update_review", review.id)
    context = {"review": review}
    return render(request, "reviews/update_review.html", context=context)
