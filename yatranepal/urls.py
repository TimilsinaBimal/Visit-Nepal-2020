"""VisitNepal2020 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePageView, name='home'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('places/', views.placeListView, name="places"),
    path('adventures/', views.adventureListView, name="adventures"),
    path('hotels/', views.hotelListView, name="hotels"),
    path('packages/', views.packageListView, name="packages"),
    path('news/', views.newsListView, name="news"),
    path('currencies/', views.currListView, name="currconv"),
    path('testimonials/', views.TestimonialListView, name="testimonials"),
    path('connect/', views.connectView, name="connect"),
    path('connect/<str:username>/', views.profileView, name="profile"),
    path('connect/<str:username>/create',
         views.ProfileCreateView.as_view(), name='create_profile'),
    path('connect/<int:pk>/edit',
         views.ProfileUpdateView.as_view(), name='edit_profile'),
    path('connect/<int:pk>/edit_core',
         views.CoreProfileUpdateView.as_view(), name='edit_core_profile'),
    path('connect/password_change', views.change_password, name="change_password"),
    path('place/<placeLink>/', views.placeDetailView, name='placeDetail'),
    path('adventure/<adventureLink>/',
         views.adventureDetailView, name='adventureDetail'),
    path('hotel/<hotelLink>/', views.hotelDetailView, name='hotelDetail'),
    path('package/<packageLink>/', views.packageDetailView, name='packageDetail'),
    path('news/<newsLink>/', views.newsDetailView, name='newsDetail'),

]
