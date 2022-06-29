from django.db import models

# Create your models here.


class SchoolQueryset(models.QuerySet):
   pass

class SchoolManager(models.Manager):
   pass

class Schoolinfo(models.Model):
   def __str__(self):
      return str(self.sch_name)
   sch_code = models.CharField(null=True, blank=True ,max_length=120)
   sch_id = models.CharField(null=True, blank=True ,max_length=120)
   sch_name = models.CharField(null=True, blank=True ,max_length=120)
   sch_email = models.CharField(null=True, blank=True ,max_length=120)
   sch_address = models.CharField(null=True, blank=True ,max_length=120)
   sch_tel = models.CharField(null=True, blank=True ,max_length=120)
   class Meta:
      pass
      #ordering = ['sch_name']
   def make_id(self):
      idlist=[]
      if Schoolinfo.objects.last():
         for i in Schoolinfo.objects.all():
            idlist.append(i.sch_id[1:])
         self.sch_id = "S"+ "%06d"%(int(max(idlist))+1)
      else:
         self.sch_id = "S000000"



class Schoolteainfo(models.Model):
   def __str__(self):
      if self.schtea_schkey:
         return str(self.schtea_schkey.sch_name) + "---" + str(self.schtea_name)
      else:
         return "---" + str(self.schtea_name)
   schtea_id = models.CharField(null=True, blank=True ,max_length=120)
   schtea_name = models.CharField(null=True, blank=True ,max_length=120)
   schtea_email = models.CharField(null=True, blank=True ,max_length=120)
   schtea_pos = models.CharField(null=True, blank=True ,max_length=120)
   schtea_tel1 = models.CharField(null=True, blank=True ,max_length=120)
   schtea_tel2 = models.CharField(null=True, blank=True ,max_length=120)
   schtea_tel3 = models.CharField(null=True, blank=True ,max_length=120)
   schtea_sch = models.CharField(null=True, blank=True ,max_length=120)
   schtea_schkey = models.ForeignKey(Schoolinfo, on_delete=models.CASCADE, null=True,blank=True)
   def make_id(self):
      idlist=[]
      if Schoolteainfo.objects.last():
         for i in Schoolteainfo.objects.all():
            idlist.append(i.schtea_id[1:])
         self.schtea_id = "H"+ "%06d"%(int(max(idlist))+1)
      else:
         self.schtea_id = "H000000"