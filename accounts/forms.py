from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from charities.models import Charity

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    selected_charity = forms.ModelChoiceField(
        queryset=Charity.objects.all(),
        required=False
    )
    charity_percentage = forms.IntegerField(
        min_value=10, max_value=100, initial=10
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=True)
        Profile.objects.create(
            user=user,
            phone=self.cleaned_data.get('phone', ''),
            selected_charity=self.cleaned_data.get('selected_charity'),
            charity_percentage=self.cleaned_data.get('charity_percentage', 10)
        )
        return user