from django import forms
from django.forms import ModelForm

from .models import *

class OutputForm(ModelForm):
    class Meta:
        model = StockOutput
        fields = '__all__'
