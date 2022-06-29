from django.urls import path
from .views import *

urlpatterns = [

    path('', teacher_home),
    path('pay/', teacher_pay_view),
    path('pay/<str:tea_id>/<int:year>/<int:month>/', teacher_pay_detail),
    path('reset', teacher_id_reset),
    path('create/', teacher_create_view),

    path('<str:tea_id>/', teacher_detail),
    
    path('<str:tea_id>/inout/<str:class_id>/', teacher_inout_detail),
    path('<str:tea_id>/update/', teacher_update_view),

]
