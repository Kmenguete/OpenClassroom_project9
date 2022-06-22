from django import forms
from . import models
from betterforms.multiform import MultiModelForm


class AskReviewForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['ticket', 'headline', 'rating', 'body']


class CreateNewReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        exclude = ('ticket',)
        fields = ['headline', 'rating', 'body']


class ReviewNewBookForm(MultiModelForm):
    form_classes = {
        'ask_review': AskReviewForm,
        'create_new_review': CreateNewReviewForm,
    }
