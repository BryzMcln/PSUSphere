from django.forms import ModelForm
from django import forms
from .models import Organization


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"