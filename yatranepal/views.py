from django.contrib.auth.mixins import LoginRequiredMixin
import math
import requests
import json
import datetime
import pyowm
from geolite2 import geolite2
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages, auth
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView
from .models import *
from .forms import *
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.


def homePageView(request):
    res = requests.get("https://visitnepal2020.com/news/")
    soup = BeautifulSoup(res.text, 'lxml')
    temp_headline = soup.select('.card-theme-news-title')
    headline = [i.text for i in temp_headline]
    newsLink = [i.lower().replace(' ', '-').replace('/', '-')
                for i in headline]

    # Currency Converter API
    def currency_converter(from_currency, to_currency, amount):
        api_key = '029b1a3324ceddd402ef'
        query = f"{from_currency}_{to_currency}"
        url = f"https://free.currconv.com/api/v7/convert?q={query}&compact=ultra&apiKey={api_key}"
        my_request = requests.get(url)
        json_file = json.loads(my_request.text)
        final_amount = json_file[query] * amount
        return final_amount

    # Currency Converter Things Here
    if request.method == 'POST':
        form = CurrencyConverterForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            from_currency = form.cleaned_data.get('from_currency')
            to_currency = form.cleaned_data.get('to_currency')
            result = currency_converter(
                from_currency, to_currency, float(amount))
            response_data = {}
            response_data['result'] = round(result, 4)
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )

    user = request.user
    my_title = zip(headline[0:7], newsLink[0:7])

    temp_adventures = Adventure.objects.all()[0:3]
    adventures = enumerate(temp_adventures, 1)

    form = CurrencyConverterForm
    temp_places = Place.objects.all()[0:3]
    places = enumerate(temp_places, 4)
    return render(
        request,
        "home.html",
        {
            "news_title": my_title,
            "form": form,
            'user': user,
            "hotels": Hotel.objects.all()[0:3],
            "places": Place.objects.all()[0:3],
            "adventures": Adventure.objects.all()[0:3],
            'n_places': places,
            'n_adventures': adventures,
            "packages": Package.objects.all()[0:3],
            "testimonials": Testimonial.objects.all()[0:2]

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
            return redirect(f'../connect/{request.user}/create/')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{form.error_messages[msg]}")

    form = SignUpForm
    return render(
        request,
        "register.html",
        context={"form": form, "error": form.error_messages}
    )


@login_required
def ProfileCreationView(request, username):
    if request.method == "POST":
        form = ProfileCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                return redirect('connect')
            except IntegrityError as e:
                return HttpResponse('<script>alert("You have already reviewed this Package.")</script>')
        else:
            return render(
                request,
                "connect/create_profile.html",
                {
                    'form': form,
                    'error': form.errors
                })

    form = ProfileCreationForm
    return render(
        request,
        "connect/create_profile.html",
        {
            'form': form,
        })


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
            'form': form
        }
    )


def logoutView(request):
    logout(request)
    return redirect('home')


# Currency Listing View
def currListView(request):
    date = datetime.date.today()
    year = f"{date.year}"
    month = f"{date:%m}"
    day = f"{date:%d}"
    my_url = f"https://www.nrb.org.np/exportForexJSON.php?YY={year}&MM={month}&DD={day}"
    currencies = json.loads(requests.get(my_url).text)
    my_list = currencies["Conversion"]["Currency"]
    my_sn = [i+1 for i in range(len(my_list))]
    BaseCurrency = [i["BaseCurrency"] for i in my_list]
    BaseValue = [i["BaseValue"] for i in my_list]
    TargetSell = [i["TargetSell"] for i in my_list]
    my_curr = zip(my_sn, BaseCurrency, BaseValue, TargetSell)

    return render(
        request,
        'currencyConverter.html',
        {
            'curr': my_curr
        }
    )


# Listing Views

def placeListView(request):
    places = Place.objects.all()
    paginator = Paginator(places, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    pages_range = range(1, page_obj.paginator.num_pages+1)
    return render(
        request,
        'listingPages/places.html',
        {
            "page_obj": page_obj,
            "total_pages": pages_range,
        }
    )


def adventureListView(request):
    adventures = Adventure.objects.all()
    paginator = Paginator(adventures, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    pages_range = range(1, page_obj.paginator.num_pages+1)
    return render(
        request,
        'listingPages/adventures.html',
        {
            "page_obj": page_obj,
            "total_pages": pages_range,
        }
    )


def hotelListView(request):
    hotels = Hotel.objects.all()
    paginator = Paginator(hotels, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    pages_range = range(1, page_obj.paginator.num_pages+1)
    return render(
        request,
        'listingPages/hotels.html',
        {
            "page_obj": page_obj,
            "total_pages": pages_range,
        }
    )


def packageListView(request):
    packages = Package.objects.all()
    paginator = Paginator(packages, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    pages_range = range(1, page_obj.paginator.num_pages+1)

    # Get data from Form
    if request.method == "GET":
        query = request.GET.get("query")
        relation = request.GET.get('relation')
        print(query, relation)
        if relation == "1":
            search_result = Package.objects.filter(packagePrice__gte=query)
            return render(
                request,
                'listingPages/package_search.html',
                {
                    'page_obj': search_result,
                    'query': query,
                    'relation': relation
                }
            )
        elif relation == "2":
            search_result = Package.objects.filter(packagePrice__lte=query)
            return render(
                request,
                'listingPages/package_search.html',
                {
                    'page_obj': search_result,
                    'query': query,
                    'relation': relation
                }
            )

    return render(
        request,
        'listingPages/packages.html',
        {
            "page_obj": page_obj,
            "total_pages": pages_range,
        }
    )


def newsListView(request):
    res = requests.get("https://visitnepal2020.com/news/")
    temp_soup = BeautifulSoup(res.text, 'lxml')
    soup = temp_soup.find_all('div', {'class': 'review-wrap__review'})
    news_title = [
        s.find('h5', {'class': 'card-theme-news-title'}).text for s in soup]
    news_image = [s.find('img').get('src') for s in soup]
    news_content = [
        s.find('p', {'class': 'card-theme-news-text'}).text for s in soup]
    news_slug = [t.lower().replace(' ', '-').replace('/', '-')
                 for t in news_title]
    news = zip(news_title, news_image, news_content, news_slug)
    # final_news = tuple(news)
    # print(final_news)

    # paginator = Paginator(final_news, 6)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    # pages_range = range(1,page_obj.paginator.num_pages+1)
    return render(
        request,
        'listingPages/news.html',
        {
            "news": news,
            # "page_obj": page_obj,
            # "total_pages": pages_range,
        }
    )


def TestimonialListView(request):
    testimonials = Testimonial.objects.all()
    paginator = Paginator(testimonials, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    pages_range = range(1, page_obj.paginator.num_pages+1)

    # Testimonial Form
    if request.method == "POST":
        form = TestimonialForm(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.name = request.user
                instance.save()
                return redirect('testimonials')

            except IntegrityError as e:
                return HttpResponse('<script>alert("You have already Submitted Testimonial.")</script>')
        else:
            return HttpResponse('<script>alert("Error Occured! Please Review your form and Submit again.")</script>')
    form = TestimonialForm
    return render(
        request,
        'listingPages/testimonials.html',
        {
            "form": form,
            "page_obj": page_obj,
            "total_pages": pages_range,
        }
    )


@login_required
def connectView(request):

    # Getting current user
    user = request.user
    user_profile = Profile.objects.get(user=user)

    # getting all statuses
    statuses = Status.objects.order_by('-current_time')

    # fetching users for each status
    status_users = [user for user in statuses]

    # fetching user image for status
    status_image = [Profile.objects.get(
        user=i.name).profileImage.url for i in status_users]

    # fetching user name for status
    status_name = [user.name.first_name + " " +
                   user.name.last_name for user in statuses]

    # fetching the username for status
    status_uname = [user.name.username for user in statuses]

    # Zipping for easy use
    status_detail = zip(statuses, status_image, status_name, status_uname)

    # updating status
    if request.method == "POST":
        form = StatusForm(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.current_time = datetime.datetime.now()
                instance.save()
                return redirect('connect')
            except:
                return HttpResponse('<script>alert("Error Occured! Please Review your form and Submit again.")</script>')
        else:
            return HttpResponse('<script>alert("Error Occured! Please Review your form and Submit again.")</script>')
    form = StatusForm

    return render(
        request,
        'connect/home.html',
        {
            'form': form,
            'status': status_detail,
            'user': user,
            'profile': user_profile
        }
    )


@login_required
def profileView(request, username):
    user = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user)
    current_user = request.user
    return render(
        request,
        'connect/profile.html',
        {
            'user': user,
            'profile': user_profile,
            'current_user': current_user
        }
    )


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['bio', 'country', 'address', 'dob', 'profileImage']
    template_name = 'connect/edit_profile.html'
    success_url = reverse_lazy('connect')


class CoreProfileUpdateView(UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'connect/edit_more_profile.html'
    success_url = reverse_lazy('connect')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'connect/change_password.html', {
        'form': form
    })


# Average Rating Calculating Function
def average_rating(reviews):
    sumRating = 0
    average_rating = 0
    for i in reviews:
        sumRating = sumRating+i.rating
    if(len(reviews) != 0):
        try:
            average_rating = round((sumRating / len(reviews)), 2)
        except:
            average_rating = 0
    else:
        average_rating = 0

    frac, whole = math.modf(average_rating)
 
    frac = round(frac, 2)
    print(frac)
    if 0.00 <= frac <= 0.13:
        average_rating = whole + 0.0
    elif 0.13 < frac <= 0.25:
        average_rating = whole + 0.25
    elif 0.25 < frac <= 0.38:
        average_rating = whole + 0.25
    elif 0.38 < frac <= 0.50:
        average_rating = whole + 0.50
    elif 0.50 < frac <= 0.63:
        average_rating = whole + 0.50
    elif 0.63 < frac <= 0.75:
        average_rating = whole + 0.75
    elif 0.75 < frac <= 0.88:
        average_rating = whole + 0.75
    else:
        average_rating = whole + 1.00

    return average_rating


# Reviews Details
five_stars_review = ["checked", "checked", "checked", "checked", "checked"]
four_stars_review = ["checked", "checked", "checked", "checked", ""]
three_stars_review = ["checked", "checked", "checked", "", ""]
two_stars_review = ["checked", "checked", "", "", ""]
one_star_review = ["checked", "", "", "", ""]


def placeDetailView(request, placeLink):
    # Getting place details from Database
    placeContent = Place.objects.get(placeSlug=placeLink)

    # Fetching To-Do list for Same place from Database
    adventure = [item.adventure for item in AdventuresInPlace.objects.filter(
        place__placeSlug=placeLink)]

    # Getting Images for places from Database
    images = [item for item in PlaceImage.objects.filter(
        place__placeSlug=placeLink)]

    # WEATHER FORECAST
    owm = pyowm.OWM('f22565e99c4ba2e70abab3885734c1b3')

    # GET CURRENT USER LOCATION
    # Getting IP ADDRESS
    my_ip = requests.get('https://api.ipify.org').text

    reader = geolite2.reader()
    location = reader.get(my_ip)
    latitude = location['location']['latitude']
    longitude = location['location']['longitude']
    try:
        observation = owm.weather_at_place(placeContent.placeName+",NP")
    except:
        observation = owm.weather_around_coords(
            latitude, longitude, limit=1)[0]

    w = observation.get_weather()
    temperature = w.get_temperature(unit='celsius')
    temperature_max = temperature['temp_max']
    temperature_min = temperature['temp_min']
    temperature_acc = temperature['temp']
    detailed_status = w.get_detailed_status()
    weather_icon = w.get_weather_icon_url()
    humidity = w.get_humidity()
    clouds = w.get_clouds()
    pressure = w.get_pressure()['press']

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
            'temperature': temperature_acc,
            'temperature_max': temperature_max,
            'temperature_min': temperature_min,
            'detailed_status': detailed_status,
            'weather_icon': weather_icon,
            'humidity': humidity,
            'clouds': clouds,
            'pressure': pressure,
            'overallRating': average_rating(reviews),
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
            'overallRating': average_rating(reviews),
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
            # 'overallRating': average_rating(reviews),
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
            'overallRating': average_rating(reviews),
            'five_stars_review': five_stars_review,
            'four_stars_review': four_stars_review,
            'three_stars_review': three_stars_review,
            'two_stars_review': two_stars_review,
            'one_star_review': one_star_review
        }
    )
