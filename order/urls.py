from django.urls import path
from .views import *

urlpatterns = [
    path('', order_view),
    path('done/', order_done_view),
    path('custom/', order_custom_view),

    path('custom/<str:order_id>/', order_custom_detail_view),
    path('custom/<str:order_id>/delete/<str:mat_id>/', order_custom_delete_view),
    path('<str:order_id>/', order_detail),
    path('<str:order_id>/odelete/', order_delete_view),
    path('<str:order_id>/delete/<str:rel_id>/', order_rel_delete),
    path('<str:inven_id>/inven/', order_inven),


    
]
