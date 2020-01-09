from django.contrib import admin
from .models import Place, Hotel, Adventure, Package, Transportation, TransportationType, Profile,AdventureToPlace,PlaceImage,Review
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.
class PlaceAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/Link", {"fields": ["placeName", "placeSlug","placetheme"]}),
        ("Place Image", {"fields": ["placeImage"]}),
        ("Place Description", {"fields": ["placeDesc"]}),
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }


class HotelAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/Link", {"fields": ["hotelName", "hotelSlug"]}),
        ("Hotel Image", {"fields": ["hotelImage"]}),
        ("Address", {"fields": ["hotelAddress"]}),
        ("Price(per Room)", {"fields": ["hotelPrice"]}),
        ("Hotel Description", {"fields": ["hotelDesc", "hotelFeatures"]}),

    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }


class AdventureAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/Link", {"fields": ["adventureName", "adventureSlug"]}),
        ("Places Image", {"fields": ["adventureImage"]}),
        ("Adventure Description", {"fields": ["adventureDesc"]}),
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }


class PackageAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/Link", {"fields": ["packageName", "packageSlug"]}),
        ("Places Image", {"fields": ["packageImage"]}),
        ("Package Description", {"fields": [
         "packageDesc", "packageFeatures"]}),
        ("Package Fare", {"fields": ["packagePrice", "placeName"]}),
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }


admin.site.register(Place, PlaceAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Adventure, AdventureAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Transportation)
admin.site.register(TransportationType)
admin.site.register(Profile)
admin.site.register(AdventureToPlace)
admin.site.register(PlaceImage)
admin.site.register(Review)