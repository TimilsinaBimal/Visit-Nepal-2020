import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm, LoginForm, ReviewForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages, auth
from django.db import IntegrityError
from .models import Place, Profile, Transportation, TransportationType, Package, Adventure, Hotel, AdventuresInPlace, PlaceImage, Review, AdventureImage, HotelImage, PackageImage
# Create your views here.

def homePageView(request):
    # res = requests.get("https://visitnepal2020.com/news/")
    # soup = BeautifulSoup(res.text, 'lxml')
    # temp_headline = soup.select('.card-theme-news-title')
    # headline = [i.text for i in temp_headline]
    # newsLink = [i.lower().replace(' ', '-') for i in headline]

    user = request.user
    # my_title = zip(headline[0:7], newsLink[0:7])

    temp_adventures = Adventure.objects.all()[0:3]
    adventures = enumerate(temp_adventures,1)

    temp_places = Place.objects.all()[0:3]
    places = enumerate(temp_places,4)
    return render(
            request,
            "home.html",
            {
                # "news_title": my_title,
                # "form": form,
                'user': user,
                "hotels": Hotel.objects.all()[0:3],
                "places": Place.objects.all()[0:3],
                "adventures": Adventure.objects.all()[0:3],
                'n_places': places,
                'n_adventures':adventures,
                "packages": Package.objects.all()[0:3],
            }
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




def loginView(request):
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
                return redirect('connect')
            else:
                return messages.error(request, "Invalid Username or Password")
        else:
            return messages.error(request, "Invalid Username or Password")

    form = LoginForm()
    user = request.user
    return render(
        request,
        'login.html',
        {
            'form':form
        }
    )



def logoutView(request):
    logout(request)
    return redirect('home')



# Listing Views

def placeListView(request):
    places = Place.objects.all()
    return render(
        request,
        'listingPages/places.html',
        {
            "place": places,
        }
    )


def adventureListView(request):
    adventures = Adventure.objects.all()
    return render(
        request,
        'listingPages/adventures.html',
        {
            "adventure": adventures,
        }
    )


def hotelListView(request):
    hotels = Hotel.objects.all()
    return render(
        request,
        'listingPages/hotels.html',
        {
            "hotel": hotels,
        }
    )


def packageListView(request):
    packages = Package.objects.all()
    return render(
        request,
        'listingPages/packages.html',
        {
            "package": packages,
        }
    )


def newsListView(request):
    res = requests.get("https://visitnepal2020.com/news/")
    temp_soup = BeautifulSoup(res.text, 'lxml')
    soup =temp_soup.find_all('div',{'class':'review-wrap__review'})
    news_title = [s.find('h5',{'class': 'card-theme-news-title'}).text for s in soup]
    news_image = [s.find('img').get('src') for s in soup]
    news_content = [s.find('p',{'class':'card-theme-news-text'}).text for s in soup]
    news_slug = [t.lower().replace(' ', '-') for t in news_title]
    news = zip(news_title, news_image ,news_content, news_slug)
    return render(
        request,
        'listingPages/news.html',
        {
            "news": news,
        }
    )



def connectView(request):
    return render(
        request,
        'connect/home.html'
    )



def profileView(request,username):
    return render(
        request,
        'connect/profile.html'
    )



# Reviews Details
five_stars_review = ["checked", "checked", "checked", "checked", "checked"]
four_stars_review = ["checked", "checked", "checked", "checked", ""]
three_stars_review = ["checked", "checked", "checked", "", ""]
two_stars_review = ["checked", "checked", "", "", ""]
one_star_review = ["checked", "", "", "", ""]



# Place Details Page View
def placeDetailView(request, placeLink):

    # Getting place details from Database
    placeContent = Place.objects.get(placeSlug=placeLink)

    # Fetching To-Do list for Same place from Database
    adventure = [item.adventure for item in AdventuresInPlace.objects.filter(
        place__placeSlug=placeLink)]

    # Getting Images for places from Database
    images = [item for item in PlaceImage.objects.filter(
        place__placeSlug=placeLink)]

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
    reviews = [item for item in Review.objects.filter(
        reviewedFor=placeContent.placeName)]
    # Profile.objects.filter(user=reviews.user)
    userProfile = []
    for item in reviews:
        userProfileList = Profile.objects.get(user__username=item.user)
        userProfile.append(userProfileList)

    placeReviews = zip(reviews, userProfile)

    return render(
        request,
        'pages/placeDetail.html',
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



def adventureDetailView(request, adventureLink):

    adventureContent = Adventure.objects.get(adventureSlug=adventureLink)

    place = [item.place for item in AdventuresInPlace.objects.filter(
        adventure__adventureSlug=adventureLink)]

    images = [item for item in AdventureImage.objects.filter(
        adventure__adventureSlug=adventureLink)]

    # Review Form
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.reviewedFor = adventureContent.adventureName
                instance.save()

            except IntegrityError as e:
                return HttpResponseRedirect('<script>alert("You have already reviewed this Adventure.")</script>')
        else:
            return HttpResponse('<script>alert("Error Occured! Please Review your form and Submit again.")</script>')

    # Handling Reviews Lists
    reviews = [item for item in Review.objects.filter(
        reviewedFor=adventureContent.adventureName)]
    # Profile.objects.filter(user=reviews.user)
    userProfile = []
    for item in reviews:
        userProfileList = Profile.objects.get(user__username=item.user)
        userProfile.append(userProfileList)

    adventureReview = zip(reviews, userProfile)

    return render(
        request,
        'pages/adventureDetail.html',
        {
            'adventure': adventureContent,
            'place': place,
            'adventureImage': images,
            'form': ReviewForm,
            'reviews': adventureReview,
            'user': request.user,
            'five_stars_review': five_stars_review,
            'four_stars_review': four_stars_review,
            'three_stars_review': three_stars_review,
            'two_stars_review': two_stars_review,
            'one_star_review': one_star_review
        }
    )



def newsDetailView(request, newsLink):
    temp_url = "https://visitnepal2020.com/{}/"
    url = temp_url.format(newsLink)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    news_title = soup.find('h3', {'class': 'modal--news__main-title'}).text
    news_figure = soup.find(
        'figure', {'class': 'review-wrap-content__figure text-center'})
    news_image = news_figure.find('img').get('src')
    news_content = soup.find('div', {'class': 'newspaper'}).text
    return render(
        request,
        'pages/newsDetails.html',
        {
            'news_title': news_title,
            'news_image': news_image,
            'news_content': news_content
        }
    )



def hotelDetailView(request, hotelLink):
    hotelContent = Hotel.objects.get(hotelSlug=hotelLink)

    images = [item for item in HotelImage.objects.filter(
        hotel__hotelSlug=hotelLink)]

    # Review Form
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.reviewedFor = hotelContent.hotelName
                instance.save()

            except IntegrityError as e:
                return HttpResponseRedirect('<script>alert("You have already reviewed this Hotel.")</script>')
        else:
            return HttpResponse('<script>alert("Error Occured! Please Review your form and Submit again.")</script>')

    # Handling Reviews Lists
    reviews = [item for item in Review.objects.filter(
        reviewedFor=hotelContent.hotelName)]
    # Profile.objects.filter(user=reviews.user)
    userProfile = []
    for item in reviews:
        userProfileList = Profile.objects.get(user__username=item.user)
        userProfile.append(userProfileList)

    hotelReview = zip(reviews, userProfile)

    return render(
        request,
        'pages/hotelDetail.html',
        {
            'hotel': hotelContent,
            'hotelImage': images,
            'form': ReviewForm,
            'reviews': hotelReview,
            'user': request.user,
            'five_stars_review': five_stars_review,
            'four_stars_review': four_stars_review,
            'three_stars_review': three_stars_review,
            'two_stars_review': two_stars_review,
            'one_star_review': one_star_review
        }
    )



def packageDetailView(request, packageLink):
    packageContent = Package.objects.get(packageSlug=packageLink)

    images = [item for item in PackageImage.objects.filter(
        package__packageSlug=packageLink)]

    # Review Form
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.reviewedFor = packageContent.packageName
                instance.save()

            except IntegrityError as e:
                return HttpResponse('<script>alert("You have already reviewed this Package.")</script>')
        else:
            return HttpResponse('<script>alert("Error Occured! Please Review your form and Submit again.")</script>')

    # Handling Reviews Lists
    reviews = [item for item in Review.objects.filter(
        reviewedFor=packageContent.packageName)]
    # Profile.objects.filter(user=reviews.user)
    userProfile = []
    for item in reviews:
        userProfileList = Profile.objects.get(user__username=item.user)
        userProfile.append(userProfileList)

    packageReview = zip(reviews, userProfile)

    return render(
        request,
        'pages/packageDetail.html',
        {
            'package': packageContent,
            'packageImage': images,
            'form': ReviewForm,
            'reviews': packageReview,
            'user': request.user,
            'five_stars_review': five_stars_review,
            'four_stars_review': four_stars_review,
            'three_stars_review': three_stars_review,
            'two_stars_review': two_stars_review,
            'one_star_review': one_star_review
        }
    )
