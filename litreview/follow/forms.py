from django import forms


class UserFollowForm(forms.Form):
    user_search = forms.CharField(max_length=50)
