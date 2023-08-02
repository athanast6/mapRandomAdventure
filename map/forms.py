# app_name/forms.py
from django import forms

class DropdownForm(forms.Form):
    choices = [('option1', 'Small'), ('option2', 'Medium'), ('option3', 'Large')]
    dropdown = forms.ChoiceField(choices=choices)
