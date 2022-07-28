from django import forms


class SearchForm(forms.Form):
    user_search = forms.CharField(max_length=50)
