from django import forms
from django.forms import ModelForm
from django.contrib.auth.views import PasswordResetForm

from .models import Individual, Organisation
from .models import Action, Deal, Order

class OrganisationAddForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields= ('name',)

class IndividualAddForm(forms.ModelForm):
    class Meta:
        model = Individual
        fields = ('name',)

class ActionAddForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ('des',)

class DealAddForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ('des',)
        
class OrderAddForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('des',)