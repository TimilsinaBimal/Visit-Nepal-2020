from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages, auth
from .models import Place, Profile, Transportation, TransportationType, Package, Adventure, Hotel,AdventureToPlace
# Create your views here.


def homePageView(request):

    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(
                    request, f"Logged in Successfully as: {username}")
                return redirect('home')
            else:
                return messages.error(request, "Invalid Username or Password")
        else:
            return messages.error(request, "Invalid Username or Password")

    form = LoginForm()
    user = request.user

    if user.is_authenticated:
        fullname = user.get_full_name()
        context = {
            "form": form,
            'user': user,
            "fullname": fullname,
            "userDetail": Profile.objects.get(user=user),
            "hotels": Hotel.objects.all()[0:3],
            "places": Place.objects.all()[0:3],
            "adventures": Adventure.objects.all()[0:3],
            "packages": Package.objects.all()[0:3],
        }
        return render(
            request,
            "home.html",
            context
        )
    else:
        return render(
            request,
            "home.html",
            {"form": form},

        )


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created: {username}")
            login(request, user)
            return redirect('home')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = SignUpForm
    return render(
        request,
        "register.html",
        context={"form": form, "error": form.error_messages}
    )


def logout(request):
    auth.logout(request)


def placeDetailView(request,placeLink):
    placeContent = Place.objects.get(placeSlug=placeLink)
    adventure = [item.adventure for item in AdventureToPlace.objects.filter(
        place__placeSlug=placeLink)]
    return render(
        request,
        'pages/places.html',
        {
            'place' : placeContent,
            'adventure': adventure
        }
    )

def adventureDetailView(request):
    return render(
        request,
        'pages/adventures.html'
    )

def hotelDetailView(request):
    return render(
        request,
        'pages/hotels.html'
    )

def packageDetailView(request):
    return render(
        request,
        'pages/packages.html'
    )
