from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


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
