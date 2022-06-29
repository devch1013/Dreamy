from django.urls import path
from .views import *

urlpatterns = [

    path('', classstat_table_view),
    #path('classstatinput', class_sch_queryinput),
    path('create/', classstat_create_view),
    path('reset/', class_data_reset),

    path('<str:class_code>/', classstat_detail_view),

    path('<str:class_code>/delete/<str:mat_name>/',mat_delete_view),
    path('<str:class_code>/update/<str:mat_name>/',mat_update_view),
    path('<str:class_code>/create/',mat_create_view),
    path('<str:class_code>/edit/',classstat_update_view),

    #path('<str:class_id>/delete/', class_delete_view),
    #path('<str:class_id>/update/', class_update_view),

]