"""
URL configuration for Performance_Optimization_in_Cloud_Computing_Using_Machine_Learning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import views as mv
from Admin import views as av
from Users import  views as uv
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',mv.index,name='index'),
    path('adminLoginForm',mv.adminLoginForm,name='adminLoginForm'),
    path('userLoginForm',mv.userLoginForm,name='userLoginForm'),
    path('userRegisterForm',mv.userRegisterForm,name='userRegisterForm'),


    path('adminLoginCheck',av.adminLoginCheck,name='adminLoginCheck'),
    path('adminHome',av.adminHome,name='adminHome'),
    path('userList',av.userList,name='userList'),
    path('activate_user',av.activate_user,name='activate_user'),
    path('deactivate_user',av.deactivate_user,name='deactivate_user'),
    
    path('log',av.log,name='log'),






    path('userRegisterCheck',uv.userRegisterCheck,name='userRegisterCheck'),
    path('userLoginCheck',uv.userLoginCheck,name='userLoginCheck'),
    path('userHome',uv.userHome,name='userHome'),
    path('training',uv.training,name='training'),
    path('prediction',uv.prediction,name='prediction'),

    

    
    
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
