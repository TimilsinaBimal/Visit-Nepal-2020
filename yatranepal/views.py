from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm, LoginForm, ReviewForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages, auth
from django.db import IntegrityError
from .models import Place, Profile, Transportation, TransportationType, Package, Adventure, Hotel,AdventureToPlace,PlaceImage,Review
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


# Reviews Details
five_stars_review= ["checked", "checked", "checked", "checked", "checked"]
four_stars_review= ["checked", "checked", "checked", "checked", ""]
three_stars_review= ["checked", "checked", "checked", "", ""]
two_stars_review= ["checked", "checked", "", "", ""]
one_star_review= ["checked", "", "", "", ""]



# Place Details Page View
def placeDetailView(request,placeLink):
    # Getting place details from Database
    placeContent = Place.objects.get(placeSlug=placeLink)

    # Fetching To-Do list for Same place from Database
    adventure = [item.adventure for item in AdventureToPlace.objects.filter(
        place__placeSlug=placeLink)]

    # Getting Images for places from Database
    images = [item for item in PlaceImage.objects.filter(place__placeSlug= placeLink)]

# Review Form
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.reviewedFor = placeContent.placeName
                instance.save()

            except IntegrityError as e:
                return HttpResponse('<script>alert("You have already reviewed this place.")</script>')
        else:
            return HttpResponse('<script>alert("Error Occured! Please Review your form and Submit again.")</script>')

    # Handling Reviews Lists
    reviews = [item for item in Review.objects.filter(reviewedFor = placeContent.placeName)]
    # Profile.objects.filter(user=reviews.user)
    userProfile=[]
    for item in reviews:
        userProfileList= Profile.objects.get(user__username=item.user)
        userProfile.append(userProfileList)

    placeReviews = zip(reviews,userProfile)

    return render(
        request,
        'pages/places.html',
        {
            'place': placeContent,
            'adventure': adventure,
            'placeImage': images,
            'form': ReviewForm,
            'reviews': placeReviews,
            'user': request.user,
            'five_stars_review': five_stars_review,
            'four_stars_review': four_stars_review,
            'three_stars_review': three_stars_review,
            'two_stars_review': two_stars_review,
            'one_star_review': one_star_review
        }
    )

# Adventure Details Page View
def adventureDetailView(request,adventureLink):

    # # Getting Adventure details from Database
    # adventureContent = Adventure.objects.get(adventureSlug=adventureLink)

    # # Fetching To-Do list for Same place from Database
    # place = [item.place for item in AdventureToPlace.objects.filter(
    #     adventure__adventureSlug=adventureLink)]

    # # Getting Images for places from Database
    # images = [item for item in adventureImage.objects.filter(
    #     adventure__adventureSlug=adventureLink)]

    # # Review Form
    # if request.method == "POST":
    #     form = ReviewForm(request.POST)
    #     if form.is_valid():
    #         instance = form.save(commit=False)
    #         instance.reviewedFor = placeContent.placeName
    #         instance.save()

    # # Handling Reviews Lists
    # reviews = [item for item in Review.objects.filter(
    #     reviewedFor=placeContent.placeName)]
    # # Profile.objects.filter(user=reviews.user)
    # userProfile = []
    # for item in reviews:
    #     userProfileList = Profile.objects.get(user__username=item.user)
    #     userProfile.append(userProfileList)

    # placeReviews = zip(reviews, userProfile)

    # return render(
    #     request,
    #     'pages/places.html',
    #     {
    #         'place': placeContent,
    #         'adventure': adventure,
    #         'placeImage': images,
    #         'form': ReviewForm,
    #         'reviews': placeReviews,
    #         'user': request.user,
    # 'five_stars_review': five_stars_review,
    # 'four_stars_review': four_stars_review,
    # 'three_stars_review': three_stars_review,
    # 'two_stars_review': two_stars_review,
    # 'one_star_review': one_star_review
#     }
    # )
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
