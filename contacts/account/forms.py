from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('username', 'name', 'phone_number', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['phone_number'].required = True
