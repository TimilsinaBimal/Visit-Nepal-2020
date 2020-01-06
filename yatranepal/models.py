from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.


class Place(models.Model):
    placeName = models.CharField(
        max_length=255, verbose_name="Name of the Place")
    placeImage = models.ImageField(
        upload_to="places/", verbose_name="Image of Place")
    placeDesc = models.TextField(verbose_name="Place Description")
    placeSlug = models.CharField(max_length=50, verbose_name="Place URL")

    def __str__(self):
        return self.placeName


class Hotel(models.Model):
    hotelName = models.CharField(
        max_length=255, verbose_name="Name of the Hotel")
    hotelAddress = models.CharField(
        max_length=255, verbose_name="Location of Hotel")
    hotelImage = models.ImageField(
        upload_to='hotels/', verbose_name="Image of Hotel")
    hotelDesc = models.TextField(verbose_name="Hotel Description")
    hotelFeatures = models.TextField(
        verbose_name="Features of Hotel(in Points)")
    hotelPrice = models.IntegerField(
        verbose_name="Price of Hotel per Room per day")
    hotelSlug = models.CharField(max_length=50, verbose_name="Hotel URL")

    def __str__(self):
        return self.hotelName


class TransportationType(models.Model):
    transportationType = models.CharField(
        max_length=255, verbose_name="Transportation Type")

    def __str__(self):
        return self.transportationType


class Transportation(models.Model):
    transportationType = models.ForeignKey(
        TransportationType, on_delete=models.CASCADE, verbose_name="TransportationType")
    placeFrom = models.CharField(max_length=200, verbose_name="Source Place")
    placeTo = models.CharField(
        max_length=200, verbose_name="Destination Place")
    fare = models.IntegerField(verbose_name="Price(NRs.)")

    def __str__(self):
        return self.placeFrom + " " + self.placeTo


class Adventure(models.Model):
    adventureName = models.CharField(
        max_length=200, verbose_name="Name of Adventure")
    adventureDesc = models.TextField(verbose_name="Adventure Description")
    adventureImage = models.ImageField(
        upload_to="adventures/", verbose_name="Adventure Image")
    adventureSlug = models.CharField(
        max_length=50, verbose_name="Adventure URL")

    def __str__(self):
        return self.adventureName


class Package(models.Model):
    packageName = models.CharField(max_length=200, verbose_name="Package Name")
    packageDesc = models.TextField(verbose_name="Package Description")
    packageImage = models.ImageField(
        upload_to="packages/", verbose_name="Package Image")
    packageSlug = models.CharField(max_length=50, verbose_name="Package URL")
    packagePrice = models.IntegerField(
        verbose_name="Package Tentative Price(NRs)")
    packageFeatures = models.TextField(verbose_name="Package Features")
    placeName = models.ManyToManyField(
        Place, verbose_name="Places that Lies in This Package")

    def __str__(self):
        return self.packageName


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Username")
    bio = models.CharField(max_length=150, verbose_name="Bio")
    country = CountryField(blank_label='Select Country')
    address = models.CharField(max_length=100, verbose_name=Address)
    phone = models.IntegerField(verbose_name="Mobile Number")
    dob = models.DateField(verbose_name="Date of Birth")

    def __str__(self):
        return self.user.username


# class Testimonial(models.Model):
#     name = models.ForeignKey(
#         'auth.User',
#         on_delete=models.CASCADE, verbose_name="Select your Name"
#     )
#     title = models.CharField(
#         max_length=500, verbose_name="Enter the Review Title")
#     review = models.TextField(verbose_name="Your Review")

#     def __str__(self):
#         return self.name
