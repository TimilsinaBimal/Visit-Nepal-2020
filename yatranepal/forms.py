import requests
import json
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Review, Testimonial, Status, Profile
from django_countries.fields import CountryField


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form__input',
                'id': 'username',
                'placeholder': 'Username'
            })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form__input',
                'id': 'password',
                'placeholder': 'password'
            })
    )

    class Meta:
        model = User
        fields = ("username", "password")

    def save(self, commit=True):
        user = super(LoginForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.password1 = self.cleaned_data['password']
        if commit:
            user.save()
        return user


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form__input',
                'id': 'first_name',
                'placeholder': 'First Name'
            })
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form__input',
                'id': 'last_name',
                'placeholder': 'Last Name'
            })
    )
    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form__input',
                'id': 'username',
                'placeholder': 'Userame'
            })
    )
    email = forms.EmailField(
        max_length=30,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form__input',
                'id': 'email',
                'placeholder': 'Email Address'
            })
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form__input',
                'id': 'password1',
                'placeholder': 'Password',
                'data-toggle': 'password'
            })
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form__input',
                'id': 'password2',
                'placeholder': 'Confirm Password',
                'data-toggle': 'password'
            })
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name",
                  "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']
        if commit:
            user.save()
        return user


# PROFILE CREATION FORM


class ProfileCreationForm(ModelForm):
    bio = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form__input',
                'id': 'bio',
                'placeholder': 'Bio'
            })
    )
    country = CountryField()
    address = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form__input',
                'id': 'address',
                'placeholder': 'Address'
            })
    )
    phone = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form__input',
                'id': 'phone',
                'placeholder': 'phone'
            })
    )
    dob = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form__input',
                'id': 'dob',
                'placeholder': 'Date of Birth'
            })
    )

    class Meta:
        model = Profile
        fields = ("bio",
                  "country", "address", "phone", "dob", "profileImage")


class ReviewForm(ModelForm):
    reviewedFor = forms.CharField(
        required=True,
        widget=forms.HiddenInput(
            attrs={
                'class': 'form__input',
                'id': 'reviewed_for',
                'placeholder': 'Reviewed For',
                'value': 'Hello'
            })
    )
    rating = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form__input',
                'id': 'rating',
                'placeholder': 'Rating(1-5)',
            })
    )
    comments = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'cols': 80,
                'rows': 8,
                'class': 'form__input',
                'id': 'comment',
                'placeholder': 'Your Review Here...',
            })
    )

    class Meta:
        model = Review
        fields = ['reviewedFor', 'rating', 'comments']


# Currency Converter
api_key = '029b1a3324ceddd402ef'
currencies = f"https://free.currconv.com/api/v7/currencies?apiKey={api_key}"
currency = json.loads(requests.get(currencies).text)
# list = currency["results"].keys()
my_list = []
# for i in list:
#     my_list.append((i, i))
# final_list = tuple(my_list)


class CurrencyConverterForm(forms.Form):
    amount = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form__input',
                'id': 'amount',
                'placeholder': 'Enter an amount',
            })
    )
    from_currency = forms.ChoiceField(
        # choices=final_list,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form__input',
                'id': 'from_currency',
            })
    )
    to_currency = forms.ChoiceField(
        # choices=final_list,
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form__input',
                'id': 'to_currency',
            })
    )


class TestimonialForm(ModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.HiddenInput(
            attrs={
                'class': 'form__input',
                'id': 'name',
                'placeholder': 'name',
                'value': 'Bimal'
            })
    )
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form__input',
                'id': 'title',
                'placeholder': 'Enter Title Here',
            })
    )
    review = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'cols': 200,
                'rows': 8,
                'class': 'form__input',
                'id': 'review',
                'placeholder': 'Your Review Here...',
            })
    )

    class Meta:
        model = Testimonial
        fields = ['title', 'review']


class StatusForm(ModelForm):
    status = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'cols': 80,
                'rows': 8,
                'class': 'posttweetta',
                'id': 'posttweetta',
                'placeholder': 'What\'s happening?',
            })
    )

    class Meta:
        model = Status
        fields = ['status']
