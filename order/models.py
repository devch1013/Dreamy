from django.db import models
from django.urls import reverse
from material.models import *


# Create your models here.
class Order(models.Model):
	def __str__(self):
		return str(self.order_id) + "---" + str(self.order_date)
	order_date = models.DateTimeField(null=True, blank=True)
	order_id = models.CharField(null=True, blank=True, max_length=120)
	order_price = models.IntegerField(null=True, blank=True)
	order_deli_price = models.IntegerField(null=True, blank=True)
	order_meth = models.CharField(null=True, blank=True ,max_length=120)
	order_acc = models.CharField(null=True, blank=True, max_length=120)
	order_user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
	order_done = models.BooleanField(default=False)
	category = models.CharField(null=True, blank=True, max_length=120)
	def get_absolute_url(self):
		return reverse('order:detail', args=[self.order_id])
	def make_id(self):
		if Order.objects.last():
			self.order_id = "O"+ "%06d"%(int(Order.objects.last().order_id[1:])+1)
		else:
			self.order_id = "O000000"
	def get_mat(self):
		return Order_Cart.objects.all().filter(order_info=self)



class Order_Cart(models.Model):
	order_date = models.DateTimeField(null=True, blank=True)
	order_info = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE)
	category = models.CharField(null=True, blank=True, max_length=120)
	mat_info = models.ForeignKey(Materialinfo, on_delete=models.SET_NULL, null=True, blank=True)
	shop = models.CharField(null=True, blank=True, max_length=120)
	order_amount = models.FloatField(null=True, blank=True)
	deli_amount = models.FloatField(null=True, blank=True)
	deli_check_date = models.DateTimeField(null=True, blank=True)
	price = models.IntegerField(null=True, blank=True)
	deli_state = models.CharField(default="결제대기중", null=True, blank=True, max_length=120)
