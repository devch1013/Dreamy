from django.urls import path
from .views import *

urlpatterns = [

    path('', School_table),

    path('reset/', School_idreset),

    path('<str:sch_id>/',School_detail_view),
    path('<str:sch_id>/schtea/',School_teacher_view),
    path('<str:sch_id>/create/',Schooltea_create_view),
    path('<str:sch_id>/<str:schtea_id>/update',Schooltea_update_view),
    path('<str:sch_id>/<str:schtea_id>/delete',Schooltea_delete_view),


]
