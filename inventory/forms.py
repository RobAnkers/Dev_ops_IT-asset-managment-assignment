# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, InventoryItem


# Form for user registration/creation, inherits from Django's UserCreationForm
class UserRegisterForm(UserCreationForm):
    # Additional field for user's email
    email = forms.EmailField()

    class Meta:
        # Define the model for the form
        model = User
        # Define the fields to be included in the login form
        fields = ["username", "email", "password1", "password2"]


# Form for inventory item creation/update
class InventoryItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
    quantity = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'min': 0}))

    class Meta:
        # Define the model for the form
        model = InventoryItem
        # Define the fields to be included in the form
        fields = ["name", "quantity", "category"]
