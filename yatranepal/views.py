from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def homePageView(request):
    return render(request, 'home.html')


def signUpView(request):
    return render(request, 'register.html')
