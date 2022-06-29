from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import *

admin.site.register(Classstatinfo)
admin.site.register(stat_mat_rel)


