from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(help_text='Required. Include + and Country Code.  Ex: +19992225555')

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password1', 'password2', )
