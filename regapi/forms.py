from django import forms
from .models import API, Event, Name_list
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CorporateForm(forms.ModelForm):
    class Meta:
        model = API
        fields = ['api_name', 'callback_url', 'redirect_url']


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class AuserForm(forms.ModelForm):
    class Meta:
        model = Name_list
        fields = ['name_list', 'event']

    def __init__(self, api, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['event'].queryset = Event.objects.filter(api=api)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_name']
