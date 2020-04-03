from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    context = {
        "title": "Hello World",
        "content": "Welcome to the Home Page! Why Perfect?",
    }
    return render(request, 'index.html', context)
