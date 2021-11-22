from django.forms import ModelForm
from clean.models import Cleaner

class CleanerForm(ModelForm):
    class Meta: 
        model = Cleaner
        fields = '__all__'