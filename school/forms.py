from django import forms
from .models import *

class SchoolModelForm(forms.ModelForm):
	sch_code = forms.CharField(required=False)
	sch_name = forms.CharField(required=True)
	sch_email = forms.CharField(required=False)
	sch_address = forms.CharField(required=False)
	sch_tel = forms.CharField(required=False)

	class Meta:
		model = Schoolinfo
		fields = ['sch_code', 'sch_name', 'sch_email', 'sch_address', 'sch_tel']


class SchoolteaForm(forms.ModelForm):
	schtea_name = forms.CharField()
	schtea_email = forms.CharField(required=False)
	schtea_pos = forms.CharField(required=False)
	schtea_tel1 = forms.CharField(required=False)
	schtea_tel2 = forms.CharField(required=False)
	class Meta:
		model = Schoolteainfo
		fields = ['schtea_name','schtea_email','schtea_pos','schtea_tel1','schtea_tel2']