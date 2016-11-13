"""healthweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from BMI.views import view_of_BMI, view_of_stat, view_of_health_home
from .views import index, add_items

urlpatterns = [
    url(r'^add/$', add_items),
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name = 'home'),
    url(r'^bmi/$', view_of_BMI, name = 'BMI'),
    url(r'^statistics/$', view_of_stat, name = 'statistics'),
    url(r'^health_home/$', view_of_health_home, name = 'health_home'),
]
