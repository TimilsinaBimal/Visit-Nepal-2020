from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.validators import MaxValueValidator, MinValueValidator
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField

# Create your models here.


class Adventure(models.Model):
    adventureName = models.CharField(
        max_length=200, verbose_name="Name of Adventure")
    adventureTheme = models.CharField(
        max_length=200, verbose_name="Theme for Adventure", default="")
    adventureDesc = models.TextField(verbose_name="Adventure Description")
    adventureImage = models.ImageField(
        upload_to="adventures/", verbose_name="Adventure Image")
    adventureSlug = models.CharField(
        max_length=50, verbose_name="Adventure URL")

    def __str__(self):
        return self.adventureName


class Place(models.Model):
    placeName = models.CharField(
        max_length=255, verbose_name="Name of the Place")
    placetheme = models.CharField(
        max_length=500, verbose_name="Theme of the Place", default="")
    placeImage = models.ImageField(
        upload_to="places/", verbose_name="Image of Place")
    placeDesc = models.TextField(verbose_name="Place Description")
    placeSlug = models.CharField(max_length=50, verbose_name="Place URL")

    def __str__(self):
        return self.placeName


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, verbose_name="Name of the Place", default=None)
    placeImage = models.ImageField(
        upload_to="places/", verbose_name="Images of the Place")

    def __str__(self):
        return self.place.placeImage.url


class AdventuresInPlace(models.Model):
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, verbose_name="Places for this Adventure", default=None)
    adventure = models.ForeignKey(
        Adventure, on_delete=models.CASCADE, verbose_name="Adventures in this Place", default=None)

    def __str__(self):
        return f"Place: {self.place.placeName}  \n Adventure: {self.adventure.adventureName}"


class Hotel(models.Model):
    hotelName = models.CharField(
        max_length=255, verbose_name="Name of the Hotel")
    hotelAddress = models.CharField(
        max_length=255, verbose_name="Location of Hotel")
    hotelTheme = models.CharField(
        max_length=500, verbose_name="Theme of the Hotel", default="")
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

    def features_as_list(self):
        return self.hotelFeatures.split('\n')


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


class Package(models.Model):
    packageName = models.CharField(max_length=200, verbose_name="Package Name")
    packageDesc = models.TextField(verbose_name="Package Description")
    packageTheme = models.CharField(
        max_length=500, verbose_name="Theme of the Package", default="")
    packageImage = models.ImageField(
        upload_to="packages/", verbose_name="Package Image")
    packageSlug = models.CharField(max_length=50, verbose_name="Package URL")
    packagePrice = models.IntegerField(
        verbose_name="Package Tentative Price(NRs)")
    packageFeatures = models.TextField(verbose_name="Package Features")

    def __str__(self):
        return self.packageName

    def package_features_as_list(self):
        return self.packageFeatures.split('\n')


class AdventureImage(models.Model):
    adventure = models.ForeignKey(
        Adventure, on_delete=models.CASCADE, verbose_name="Name of the Adventure", default="")
    adventureImages = models.ImageField(
        upload_to="adventures/", verbose_name="Image of the adventure")

    def __str__(self):
        return self.adventure.adventureName


class HotelImage(models.Model):
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, verbose_name="Name of the Hotel", default="")
    hotelImages = models.ImageField(
        upload_to="hotels/", verbose_name="Image of the Hotel")

    def __str__(self):
        return self.hotel.hotelName


class PackageImage(models.Model):
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, verbose_name="Name of the package", default="")
    packageImages = models.ImageField(
        upload_to="packages/", verbose_name="Image of the Package")

    def __str__(self):
        return self.package.packageName


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Username")
    bio = models.CharField(max_length=150, verbose_name="Bio")
    country = CountryField(blank_label='Select Country')
    address = models.CharField(max_length=100, verbose_name="Address")
    phone = models.IntegerField(verbose_name="Mobile Number")
    dob = models.DateField(verbose_name="Date of Birth")
    # profileLink = user.username
    profileImage = models.ImageField(
        upload_to="users/", verbose_name="Profile Picture", default="")

    def __str__(self):
        return self.user.username


class Review(models.Model):
    user = CurrentUserField()
    reviewedFor = models.CharField(max_length=200, verbose_name="Reviewed For")
    rating = models.PositiveIntegerField(validators=[MinValueValidator(
        1), MaxValueValidator(5)], verbose_name="Your Rating on 5")
    comments = models.CharField(max_length=600, verbose_name="Comment")

    def __str__(self):
        return f"{self.user.username} Reviewed {self.reviewedFor}"

    class Meta:
        unique_together = ('user', 'reviewedFor')


class Testimonial(models.Model):
    name = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="User", default="")
    title = models.CharField(
        max_length=500, verbose_name="Enter the Testimonial Title")
    review = models.TextField(verbose_name="Your Message")

    def __str__(self):
        return self.name.username
