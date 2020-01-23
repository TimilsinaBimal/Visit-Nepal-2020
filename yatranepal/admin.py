from django.contrib import admin
from .models import *
from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.


class AdventuresInPlaceInline(admin.TabularInline):
    model = AdventuresInPlace


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage


class PlaceAdmin(admin.ModelAdmin):
    inlines = [PlaceImageInline, AdventuresInPlaceInline]
    fieldsets = [
        ("Title/Link", {"fields": ["placeName", "placeSlug", "placetheme"]}),
        ("Place Image", {"fields": ["placeImage"]}),
        ("Place Description", {"fields": ["placeDesc"]}),
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }


class HotelImageInline(admin.TabularInline):
    model = HotelImage


class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImageInline]
    fieldsets = [
        ("Title/Link", {"fields": ["hotelName", "hotelSlug", "hotelTheme"]}),
        ("Hotel Image", {"fields": ["hotelImage"]}),
        ("Address", {"fields": ["hotelAddress"]}),
        ("Price(per Room)", {"fields": ["hotelPrice"]}),
        ("Hotel Description", {"fields": ["hotelDesc", "hotelFeatures"]}),

    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }


class AdventureImageInline(admin.TabularInline):
    model = AdventureImage


class AdventureAdmin(admin.ModelAdmin):
    inlines = [AdventureImageInline, AdventuresInPlaceInline]
    fieldsets = [
        ("Title/Link", {"fields": ["adventureName",
                                   "adventureSlug", "adventureTheme"]}),
        ("Places Image", {"fields": ["adventureImage"]}),
        ("Adventure Description", {"fields": ["adventureDesc"]}),
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }


class PackageImageInline(admin.TabularInline):
    model = PackageImage


class PackageAdmin(admin.ModelAdmin):
    inlines = [PackageImageInline]
    fieldsets = [
        ("Title/Link",
         {"fields": ["packageName", "packageSlug", "packageTheme"]}),
        ("Places Image", {"fields": ["packageImage"]}),
        ("Package Description", {"fields": [
         "packageDesc", "packageFeatures"]}),
        ("Package Fare", {"fields": ["packagePrice"]}),
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
admin.site.register(Review)
admin.site.register(Testimonial)
