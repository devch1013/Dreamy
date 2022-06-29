from django.db import models
from material.models import *

# Create your models here.
class Classstatinfo(models.Model):
   def __str__(self):
      return str(self.class_title)
   class_code = models.CharField(null=True,max_length=120)
   class_title = models.CharField(null=True,max_length=120)
   class_detail = models.TextField(null=True, blank=True)
   class_file_recipe = models.FileField(upload_to="class_data/recipe/",null=True, blank=True)
   class_file_image = models.FileField(upload_to="class_data/class_image/",null=True, blank=True)
   def make_id(self):
      idlist=[]
      if Classstatinfo.objects.last():
         for i in Classstatinfo.objects.all():
            idlist.append(i.class_code[1:])
         self.class_code = "D"+ "%06d"%(int(max(idlist))+1)
      else:
         self.class_code = "D000000"



class stat_mat_rel(models.Model):
   def __str__(self):
      if self.mat_statkey:
         return str(self.stat_mat) + "----" + str(self.mat_statkey.mat_name)
      else: return ""
   stat_mat = models.ForeignKey(Classstatinfo, on_delete=models.CASCADE, null=True, blank=True)
   stat_mat_str = models.CharField(null=True, blank=True, max_length=120)
   mat_statkey = models.ForeignKey(Materialinfo, on_delete=models.SET_NULL, null=True, blank=True)
   mat_stat = models.CharField(null=True,blank=True, max_length=120)
   stat_mat_amount = models.FloatField(null=True, blank = True)
   stat_mat_unit = models.CharField(blank=True,null=True, max_length=120)
   mat_unit = models.CharField(blank=True,null=True, max_length=120)
   category = models.CharField(blank=True,null=True, max_length=120)
   memo = models.CharField(blank=True,null=True, max_length=120)

