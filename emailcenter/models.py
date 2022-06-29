from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
from school.models import Schoolinfo

User = settings.AUTH_USER_MODEL

# Create your models here.
class Emailinfo(models.Model):
	def __str__(self):
		return str(self.email_title) +"---"+ str(self.email_receiver) +"---"+ str(self.email_sendtime)
	email_title = models.CharField(null=True, blank=True ,max_length=120)
	email_content = models.TextField(null=True, blank=True)
	email_receiver = models.CharField(null=True,max_length=120)
	email_sendtime = models.DateTimeField(null=True, blank=True)
	email_school = models.ForeignKey(Schoolinfo, on_delete=models.SET_NULL, blank=True, null=True)
	
class EmailFiles(models.Model):
	def __str__(self):
		return str(self.emailkey.email_title) + "---" + str(self.email_file.name)

	emailkey = models.ForeignKey(Emailinfo, on_delete=models.CASCADE)
	email_file = models.FileField(upload_to="email_file/email_tempfiles/", null=True, blank=True)