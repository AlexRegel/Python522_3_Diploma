"""
URL configuration for techlog_tools_spparts project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from techlog_tools import views
# from telog_spparts import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # registration, Authorization
    path('registr/', views.registr_user, name='registruser'),
    path('exitapp/', views.exitapp_user, name='exitappuser'),
    path('loginapp/', views.login_user, name='loginuser'),
    # include urls
    path('techlog_tools/', include('techlog_tools.urls')),
    path('telog_spparts/', include('telog_spparts.urls')),
]
# для 'repairs/' name='createautorepairs'
# Здесь 'telog_spparts/' конкатенируется с 'repairs/',
# т.е. с адресом пути в urls приложения, задействовав написанную
# там функцию, как указано views.create_repairs.


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# print('Вывод содержимого переменной
# "urlpatterns":  ', urlpatterns)
# telog_spparts/
