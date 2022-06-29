from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime

User = settings.AUTH_USER_MODEL

# Create your models here.
class Materialinfo(models.Model):
   def __str__(self):
      return str(self.mat_name)


   category = models.CharField(null=True, blank=True ,max_length=120)
   mat_id = models.CharField(null=True, blank=True ,max_length=120)
   mat_name = models.CharField(null=True,max_length=120)
   mat_shop = models.CharField(null=True, blank=True ,max_length=120)
   mat_link = models.CharField(null=True, blank=True ,max_length=500)
   mat_price = models.CharField(null=True, blank=True ,max_length=120)
   mat_loc = models.CharField(null=True, blank=True ,max_length=120)
   mat_inven = models.FloatField(null=True, blank=True, default=0)
   mat_unit = models.CharField(null=True, blank=True, max_length=120)
   mat_memo = models.CharField(null=True, blank=True, max_length=120)
   def make_id(self):
      idlist=[]
      if Materialinfo.objects.last():
         for i in Materialinfo.objects.all():
            idlist.append(i.mat_id[1:])
         self.mat_id = "M"+ "%06d"%(int(max(idlist))+1)
      else:
         self.mat_id = "M000000"



