from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
from school.models import *
from teacher.models import *
from classstatd.models import *
from material.models import *
from order.models import *

# Create your models here.
User = settings.AUTH_USER_MODEL


class Classinfo(models.Model):
   def __str__(self):
      return str(self.class_id) + "---" + str(self.class_sch) + "---" + str(self.class_stat)
   user = models.ForeignKey(User, default=1, null=True,  on_delete=models.SET_NULL)
   class_id = models.CharField(null=True, blank=True, max_length=120)
   class_date = models.DateField(auto_now=False, blank=True, auto_now_add=False, null=True)
   class_cate = models.CharField(null=True, blank=True,max_length=120)
   class_minicate = models.CharField(null=True, blank=True,max_length=120)
   class_stat = models.CharField(null=True, blank=True,max_length=120)
   class_statkey = models.ForeignKey(Classstatinfo, on_delete=models.SET_NULL, null=True, blank=True)
   class_stunum = models.CharField(null=True, blank=True,max_length=120)
   class_time = models.CharField(null=True, blank=True,max_length=120)
   class_place = models.CharField(null=True, blank=True,max_length=120)
   class_count = models.IntegerField(null=True, blank=True, default=1)
   class_sch = models.CharField(null=True, blank=False,max_length=120)
   class_schkey = models.ForeignKey(Schoolinfo, on_delete=models.SET_NULL, null=True, blank=True)
   class_tea = models.CharField(null=True, blank=True,max_length=120)
   class_teakey = models.ForeignKey(Teacherinfo, on_delete=models.SET_NULL, null=True,blank=True)
   memo = models.CharField(null=True, blank=True,max_length=1000)
   class_confirm = models.CharField(null=True, blank=True,max_length=120)
   timestamp_progress = models.DateTimeField(null=True, blank=True)
   user_progress = models.CharField(null=True, blank=True,max_length=120)
   timestamp_memo = models.DateTimeField(null=True, blank=True)
   user_memo = models.CharField(null=True, blank=True,max_length=120)

   schteakey = models.ForeignKey(Schoolteainfo,on_delete=models.SET_NULL, null=True,blank=True)
   schtea = models.CharField(null=True, blank=True,max_length=120)



   class_3 = models.CharField(null=True, blank=True,max_length=120)

   class_price = models.IntegerField(null=True, blank=True,default=0)
   class_tea_price = models.IntegerField(null=True, blank=True, default=0)

   class_order = models.BooleanField(default=False)
   class_deli = models.BooleanField(default=False)

   class_pay = models.CharField(null=True, blank=True,max_length=120)


   class_mani = models.BooleanField(default=False)
   class_div = models.BooleanField(default=False)
   class_taken = models.BooleanField(default=False)
   class_done = models.BooleanField(default=False)
   class_re_done = models.BooleanField(default=False)
   class_doc_plan = models.BooleanField(default=False)
   class_doc_preestim = models.BooleanField(default=False)
   class_doc_preestim_meth = models.CharField(null=True, blank=True, max_length=120)
   class_doc_tea = models.BooleanField(default=False)
   class_doc_finestim = models.BooleanField(default=False)
   class_cal_meth = models.CharField(null=True, blank=True,max_length=120)
   class_deposit_check = models.BooleanField(default=False)


   class_process = models.CharField(null=True, blank=True, default="진행X", max_length=120)

   class_file_preestim = models.FileField(upload_to="class_file/preestim/", null=True, blank=True)
   class_file_plan = models.FileField(upload_to="class_file/plan/", null=True, blank=True)
   class_file_tea = models.FileField(upload_to="class_file/tea/", null=True, blank=True)
   class_file_finestim = models.FileField(upload_to="class_file/finestim/", null=True, blank=True)
   class_file_cal = models.FileField(upload_to="class_file/cal/", null=True, blank=True)

   class_tea_inout = models.CharField(default="반출미완료", null=True, blank=True,max_length=120)
   class_tea_inout_date = models.DateTimeField(null=True, blank=True)

   

   def make_id(self):
      if Classinfo.objects.last():
         self.class_id = "C"+ "%06d"%(int(Classinfo.objects.last().class_id[1:])+1)
      else:
         self.class_id = "C000000"

   def new_recipe_check(self):
      if stat_mat_rel.objects.all().filter(stat_mat=self.class_statkey):
         return False
      elif self.class_statkey==None:
         return False
      else:
         return True


class dyna_mat_rel(models.Model):
   def __str__(self):
      return str(self.dyna_mat.class_id) + "----" + str(self.dyna_mat.class_statkey.class_title) + "----" + str(self.mat_dyna.mat_name)
   rel_id = models.CharField(null=True, blank = True, max_length = 120)
   dyna_mat = models.ForeignKey(Classinfo, on_delete=models.CASCADE, null=True, blank=True)
   dyna_mat_num = models.CharField(null=True, blank = True, max_length = 120, default="0")
   mat_dyna = models.ForeignKey(Materialinfo, on_delete=models.SET_NULL, null=True, blank=True)
   order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
   status = models.CharField(default="준비중",null=True, blank=True,max_length=120)
   taken = models.BooleanField(default=False)
   mat_manu_done = models.BooleanField(default=False)
   mat_div_done = models.BooleanField(default=False)
   tool_re = models.BooleanField(default=False)
   def make_id(self):
      if dyna_mat_rel.objects.last():
         self.rel_id = "R"+ "%07d"%(int(dyna_mat_rel.objects.last().rel_id[1:])+1)
      else:
         self.rel_id = "R0000000"


class Teacherinoutinfo(models.Model):
   category = models.CharField(max_length=120)
   inout_date= models.DateTimeField(auto_now=False, blank=True, auto_now_add=False, null=True)
   inout_class = models.ForeignKey(Classinfo, on_delete=models.SET_NULL, null=True, blank=True)
   inout_teacher = models.ForeignKey(Teacherinfo, on_delete=models.CASCADE, null=True)
   inout_status = models.CharField(default='미완료', max_length=100)


class Teacherpay_monthly(models.Model):
   def __str__(self):
      return str(self.tp_year) + "----" + str(self.tp_month) + "----" + str(self.tp_teakey.tea_name)
   tp_teakey = models.ForeignKey(Teacherinfo, on_delete=models.SET_NULL, null=True)
   tp_year = models.IntegerField(null=True, blank=True)
   tp_month = models.IntegerField(null=True, blank=True)
   tp_monthly_pay = models.IntegerField(null=True,blank=True)
   def monthly_cal(self):
      self.tp_monthly_pay = 0
      for i in Teacherpay.objects.all().filter(tp_monthly=self):
         self.tp_monthly_pay += i.tp_pay


class Teacherpay(models.Model):
   def __str__(self):
      return str(self.tp_monthly.tp_year) + "----" + str(self.tp_monthly.tp_month)+ "----" + str(self.tp_monthly.tp_teakey.tea_name) + "----" + str(self.tp_content)
   tp_classkey = models.ForeignKey(Classinfo, on_delete=models.CASCADE, null=True)
   tp_monthly = models.ForeignKey(Teacherpay_monthly, on_delete=models.SET_NULL, null=True)
   tp_pay = models.IntegerField(null=True, blank=True)
   tp_tax = models.IntegerField(null=True, blank=True)
   tp_atax = models.IntegerField(null=True, blank=True)
   tp_content = models.CharField(null=True, blank = True, max_length = 120)
   def tax_cal(self):
      self.tp_tax = self.tp_pay * 0.033
      self.tp_atax = self.tp_pay * 0.967

