"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.conf import settings
from .views import *
from order.views import *
from classd.views import *
from django.views.static import serve
from django.conf.urls import url



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', logo_page),
    path('home/', home_page),
    path('clear/', clear_page),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login_1.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('class/', include('classd.urls')),
    path('school/', include('school.urls')),
    path('inventory/', include('material.urls')),
    path('class_data/', include('classstatd.urls')),
    path('teacher/', include('teacher.urls')),
    path('order/', include('order.urls')),
    path('delivery/', delivery_view),
    path('delivery/<str:order_id>/<str:mat_id>/', delivery_check_view),
    path('delivery2/', delivery2_view),
    path('teacherin/', teacherin_view),
    path('teacherout/', teacherout_view),
    path('teacherin/<str:class_id>/', teacherin_detail_view),
    path('teacherout/<str:class_id>/', teacherout_detail_view),
    path('email/',include('emailcenter.urls')),
    
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "main.views.error_404"
handler500 = "main.views.error_500"