from django import forms
from .models import Visitor, Purpose

class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'company', 'purpose', 'check_out', 'host']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'})
        }

class PurposeForm(forms.ModelForm):
    class Meta:
        model = Purpose
        fields = ['name', 'description']