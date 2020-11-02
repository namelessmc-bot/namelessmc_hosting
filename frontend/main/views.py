from django.shortcuts import render
# from django.http import HttpResponse
from users.models import Website, User

def home(request):
    context = {
        "count_users": User.objects.count(),
        "count_websites": Website.objects.count()
    }
    return render(request, 'main/index.html', context=context)
