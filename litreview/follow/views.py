from django.contrib.auth.decorators import login_required


@login_required
def subscriptions(request):
    pass


@login_required
def search_users(request):
    pass
