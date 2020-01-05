from django import forms


class LoginForm(forms.Form):
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


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form__input',
                'id': 'username',
                'placeholder': 'Username'
            })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form__input',
                'id': 'email',
                'placeholder': 'Email'
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
