from django import forms  
from .models import User


class LoginForm(forms.Form):
    phone_number = forms.CharField(required=True, max_length = 10)
    password = forms.CharField(required=True, max_length = 24)


class SignUpForm(forms.Form):
    phone_number = forms.CharField(required=True, min_length = 10, max_length = 10)
    first_name = forms.CharField(required=True, min_length = 3, max_length = 24)
    last_name = forms.CharField(required=True, min_length = 3, max_length = 24)
    password = forms.CharField(required=True, min_length = 3, max_length = 24)
