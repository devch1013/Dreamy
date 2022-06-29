from django import forms
from .models import *

class EmailForm(forms.ModelForm):
	email_title = forms.CharField(required=True)
	email_content = forms.CharField(required=True)
	email_receiver = forms.CharField(required=True)

	class Meta:
		model = Emailinfo
		fields = ['email_title', 'email_content', 'email_receiver']
