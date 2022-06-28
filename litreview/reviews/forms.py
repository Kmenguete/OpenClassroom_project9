from django import forms
from . import models


class AskReviewForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['ticket', 'headline', 'rating', 'body']
