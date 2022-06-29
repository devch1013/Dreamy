from django import forms
from .models import *
from school.models import Schoolinfo
from teacher.models import Teacherinfo
from classstatd.models import *



class dyna_mat_relForm(forms.Form):
	dyna_mat_num = forms.CharField()
	status = forms.CharField()
	mat_manu_done = forms.BooleanField()
	mat_div_done = forms.BooleanField()

class ClassModelForm(forms.ModelForm):
	class_date = forms.DateField(required=False)
	class_cate = forms.CharField(required=False)
	class_sch = forms.CharField(required=False)
	class_tea = forms.CharField(required=False)
	class_stat = forms.CharField(required=False)

	class_minicate = forms.CharField(required=False)
	class_confirm = forms.CharField(required=True)

	class_price = forms.IntegerField(required=False)
	class_tea_price = forms.IntegerField(required=False)

	class_count = forms.IntegerField(required=False)
	class_stunum = forms.CharField(required=False)
	class_time = forms.CharField(required=False)
	class_place = forms.CharField(required=False)
	memo = forms.CharField(required=False)
	class Meta:
		model = Classinfo
		fields = ['class_date','class_sch','class_cate', 'class_stat','class_price','class_tea_price', 'class_tea','class_count','class_stunum','class_time','class_place','memo', 'class_confirm', 'class_minicate']





class ClassTableCheckForm(forms.ModelForm):
	class_ready = forms.BooleanField(required=False)
	class_taken = forms.BooleanField(required=False)
	class_done = forms.BooleanField(required=False)
	class_doc_plan = forms.BooleanField(required=False)
	class_doc_preestim = forms.BooleanField(required=False)
	class_doc_preestim_meth = forms.CharField(required=False)
	class_doc_tea = forms.BooleanField(required=False)
	class_doc_finestim = forms.BooleanField(required=False)
	class_cal_meth = forms.CharField(required=False)
	class_deposit_check = forms.BooleanField(required=False)
	class_confirm = forms.CharField(required=False)
	class_3 = forms.CharField(required=False)
	class_satisfaction = forms.IntegerField(required=False)
	class_price = forms.IntegerField(required=False)
	class_tea_price = forms.IntegerField(required=False)
	class_done = forms.BooleanField(required=False)
	class_pay = forms.CharField(required=False)
	schtea = forms.CharField(required=False)

	class Meta:
		model = Classinfo
		fields = ['memo', 'class_div','class_taken','class_mani','class_re_done', 'class_doc_plan', 'class_pay',
		'class_doc_preestim','class_doc_preestim_meth','class_doc_tea','class_doc_finestim','class_cal_meth',
		'class_deposit_check', 'class_confirm', 'class_3', 'class_satisfaction', 'class_price','class_tea_price', 'class_done','schtea']

