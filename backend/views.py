from django.shortcuts import render
# from django.http import HttpResponse


def explore_page(request):
    return render(request, 'explore.html')


def landing_page(request):
    return render(request, 'landing.html')
