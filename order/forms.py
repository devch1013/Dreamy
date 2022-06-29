from django import forms
from .models import *
from school.models import Schoolinfo
from teacher.models import Teacherinfo
from classstatd.models import *


class OrderForm(forms.ModelForm):
	
	order_price = forms.IntegerField()

	order_acc = forms.CharField()
	class Meta:
		model = Order
		fields = ['order_price','order_acc']

class deli_check_Form(forms.ModelForm):
	deli_state = forms.CharField(required=True)
	deli_amount = forms.FloatField(required=True)
	class Meta:
		model = Order_Cart
		fields = ['deli_state', 'deli_amount']