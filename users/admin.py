from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Messenger)

class CustomUserAdmin(UserAdmin):
    # fieldsets : 관리자 리스트 화면에서 출력될 폼 설정 부분
    UserAdmin.fieldsets[1][1]['fields']+=('user_name','profile_image', 'user_position','user_tea_id','tea_password','tea_id')
    # add_fieldsets : User 객체 추가 화면에 출력될 입력 폼 설정 부분
    UserAdmin.add_fieldsets += (
        (('Additional Info'),{'fields':('user_name','profile_image', 'user_position','user_tea_id','tea_password','tea_id')}),
    )