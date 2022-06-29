from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# AbstractUser를 상속한다.
class User(AbstractUser):
   POSITION_CHOICE=(
      ("원장","원장"),
      ("부원장","부원장"),
      ("소장","소장"),
      ("관리자","관리자"),
      ("센터장","센터장"),
      ("팀장","팀장"),
      ("실장","실장"),
      ("알바","알바"),
      ("인턴","인턴"),
      ("강사","강사"),
      )

   user_name = models.CharField(blank=True, max_length=120)
   user_position = models.CharField(choices=POSITION_CHOICE,blank=True, max_length=120)
   profile_image = models.ImageField(blank=True,null=True, upload_to='image/',)
   user_tea_id = models.CharField(blank=True, null=True, max_length=120)
   tea_password = models.CharField(blank=True, null=True, max_length=120)
   tea_id = models.CharField(blank=True, null=True, max_length=120)


class Messenger(models.Model):
   todo_memo = models.CharField(blank=True, null=True,max_length=1000)
   todo_memo_user = models.CharField(blank=True, null=True,max_length=120)
   todo_memo_time = models.DateTimeField(blank=True, null=True)
   order_memo = models.CharField(blank=True, null=True,max_length=1000)
   order_memo_user = models.CharField(blank=True, null=True,max_length=120)
   order_memo_time = models.DateTimeField(blank=True, null=True)
   
