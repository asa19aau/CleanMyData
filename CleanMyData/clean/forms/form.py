from django import forms
from django.forms import ModelForm, ClearableFileInput
from clean.models import Cleaner

class CleanerForm(ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    
    class Meta: 
        model = Cleaner
        fields = '__all__'