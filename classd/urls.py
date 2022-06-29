from django.urls import path
from .views import *


urlpatterns = [

    path('', class_home),


    path('<str:class_id>/', class_detail_view),
    path('<str:class_id>/delete/', class_delete_view),
    path('<str:class_id>/update/', class_update_view),
    

]
