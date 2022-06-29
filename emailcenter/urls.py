from django.urls import path
from .views import *


urlpatterns = [

    path('', email_home),
    path('email1/',email_page1),
    path('email2/',email_page2),
    path('email3/',email_page3),
    path('email4/',email_page4),
    

]
