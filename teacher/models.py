from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
import random
from users.models import User



# Create your models here.

class TeacherQuerySet(models.QuerySet):
   pass
class Teacherinfo(models.Model):
   def __str__(self):
      return str(self.tea_name)
   tea_id = models.CharField(null=True, blank=True ,max_length=120)
   tea_name = models.CharField(null=True, blank=True ,max_length=120)
   tea_email = models.CharField(null=True, blank=True ,max_length=120)
   tea_tel = models.CharField(null=True, blank=True ,max_length=120)
   tea_prof = models.CharField(null=True, blank=True ,max_length=120)
   tea_address = models.CharField(null=True, blank=True ,max_length=120)
   tea_bankacc = models.CharField(null=True, blank=True ,max_length=120)
   tea_bankname = models.CharField(null=True, blank=True ,max_length=120)
   tea_next_visit = models.DateField(auto_now=False, blank=True, auto_now_add=False, null=True)
   #timestamp = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(auto_now=True, null=True, blank=True)
   tea_doc_cv = models.FileField(upload_to="tea_doc/cv/", null=True, blank=True)
   tea_doc_card = models.FileField(upload_to="tea_doc/card/", null=True, blank=True)
   tea_doc_bankacc = models.FileField(upload_to="tea_doc/bankacc/", null=True, blank=True)
   tea_doc_agree = models.FileField(upload_to="tea_doc/agree/", null=True, blank=True)
   tea_doc_sign = models.FileField(upload_to="tea_doc/sign/", null=True, blank=True)
   class Meta:
      ordering = ['tea_name']
   def make_id(self):
      idlist=[]
      if Teacherinfo.objects.last():
         for i in Teacherinfo.objects.all():
            idlist.append(i.tea_id[1:])
         self.tea_id = "T"+ "%06d"%(int(max(idlist))+1)
      else:
         self.tea_id = "T000000"

   def make_user(self):
      random_number_id = random.randrange(0, 10000)
      while User.objects.all().filter(tea_id=random_number_id):
         random_number_id = random.randrange(0, 10000)
      random_number_pass = random.randrange(0, 10000)
      while User.objects.all().filter(tea_password=random_number_pass):
         random_number_pass = random.randrange(0, 10000)

      user = User.objects.create_user(username=str(self.tea_name) + str(random_number_id),password=random_number_pass,user_position = "강사",user_tea_id=self.tea_id,user_name=self.tea_name,tea_id=random_number_id,tea_password=random_number_pass)
      user.save()

