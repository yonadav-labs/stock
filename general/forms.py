from django import forms
from django.forms import ModelForm
from django.forms.utils import ErrorList

from .models import *

class OutputForm(ModelForm):
    class Meta:
        model = OfferList
        fields = '__all__'
 
    def clean(self):
        shares_max = self.cleaned_data.get('shares_max')
        shares_min = self.cleaned_data.get('shares_min')

        if shares_max < shares_min:
            self._errors['shares_max'] = ErrorList([''])
            self._errors['shares_min'] = ErrorList([''])
            raise forms.ValidationError("MIN TO BUY must be less than or equal to SHARES OFFERED")

        return self.cleaned_data
