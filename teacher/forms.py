from django import forms
from .models import *


class TeacherdetailForm(forms.ModelForm):
	tea_email = forms.CharField(required=False)
	tea_tel = forms.CharField(required=False)
	tea_prof = forms.CharField(required=False)
	tea_address = forms.CharField(required=False)
	tea_bankacc = forms.CharField(required=False)
	tea_bankname = forms.CharField(required=False)
	tea_next_visit = forms.DateField(required=False)
	
	class Meta:
		model = Teacherinfo
		fields = ['tea_email', 'tea_tel', 'tea_prof', 'tea_address',
		 'tea_bankacc', 'tea_bankname', 'tea_next_visit']

class TeacherCreateForm(forms.ModelForm):
	tea_name = forms.CharField(required=True)
	tea_prof = forms.CharField(required=False)
	tea_tel = forms.CharField(required=False)
	tea_email = forms.CharField(required=False)
	tea_address = forms.CharField(required=False)
	tea_bankname = forms.CharField(required=False)
	tea_bankacc = forms.CharField(required=False)
	class Meta:
		model = Teacherinfo
		fields = ['tea_name','tea_email', 'tea_tel', 'tea_prof', 'tea_address', 'tea_bankacc', 'tea_bankname']

class tea_doc_cv_form(forms.ModelForm):
	tea_doc_cv = forms.FileField()
	class Meta:
		model =Teacherinfo
		fields =['tea_doc_cv']

class tea_doc_card_form(forms.ModelForm):
	tea_doc_card = forms.FileField()
	class Meta:
		model =Teacherinfo
		fields =['tea_doc_card']

class tea_doc_bankacc_form(forms.ModelForm):
	tea_doc_bankacc = forms.FileField()
	class Meta:
		model =Teacherinfo
		fields =['tea_doc_bankacc']

class tea_doc_agree_form(forms.ModelForm):
	tea_doc_agree = forms.FileField()
	class Meta:
		model =Teacherinfo
		fields =['tea_doc_agree']

class tea_doc_sign_form(forms.ModelForm):
	tea_doc_sign = forms.FileField()
	class Meta:
		model =Teacherinfo
		fields =['tea_doc_sign']