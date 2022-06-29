from django import forms
from .models import *


class ClassstatForm(forms.ModelForm):

   class_title = forms.CharField()
   class_detail = forms.CharField(required=False)

   class Meta:
      model = Classstatinfo
      fields = ['class_title',  'class_detail']

class stat_mat_Form(forms.ModelForm):
   mat_stat = forms.CharField(required=True)
   stat_mat_amount = forms.FloatField(required=False)
   stat_mat_unit = forms.CharField(required=False)
   category = forms.CharField(required=False)
   mat_unit = forms.CharField(required=False)
   memo = forms.CharField(required=False)
   class Meta:
      model = stat_mat_rel
      fields = ['mat_stat', 'stat_mat_amount','stat_mat_unit','category','mat_unit','memo']

class stat_mat_update_Form(forms.ModelForm):
   stat_mat_amount = forms.FloatField(required=False)
   stat_mat_unit = forms.CharField(required=False)
   memo = forms.CharField(required=False)
   class Meta:
      model = stat_mat_rel
      fields = [ 'stat_mat_amount','stat_mat_unit','memo']

class class_file_image_form(forms.ModelForm):
   class_file_image = forms.FileField(required=False)
   class Meta:
      model =Classstatinfo
      fields =['class_file_image']

class class_file_recipe_form(forms.ModelForm):
   class_file_recipe = forms.FileField(required=False)
   class Meta:
      model =Classstatinfo
      fields =['class_file_recipe']