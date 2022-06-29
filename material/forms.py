from django import forms
from .models import *


class MaterialForm(forms.ModelForm):
   mat_name = forms.CharField()
   category = forms.CharField()
   mat_shop = forms.CharField(required=False)
   mat_link = forms.CharField(required=False)
   mat_price = forms.CharField(required=False)
   mat_loc = forms.CharField(required=False)
   mat_inven = forms.FloatField(required=False)
   mat_unit = forms.CharField()
   mat_memo = forms.CharField(required=False)
   class Meta:
      model = Materialinfo
      fields = ['category','mat_name', 'mat_shop', 'mat_price','mat_loc', 'mat_inven', 'mat_unit', 'mat_link', 'mat_memo']
