from django.urls import path
from .views import *

urlpatterns = [
    path('', material_table),
    path('create/', material_create_view),
    path('reset/', material_reset_view),
    path('<str:mat_id>/delete/', material_delete_view),
    path('<str:mat_id>/update/', material_update_view),
    

]
