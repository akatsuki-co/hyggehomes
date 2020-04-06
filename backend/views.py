from django.shortcuts import render
# from django.http import HttpResponse


def home_page(request):
    return render(request, 'home_page.html')

def landing_page(request):
    return render(request, 'landing.html')
