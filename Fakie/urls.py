"""Fakie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import (path,include)
from users.views import RegisterView, activate_user_view
from django.conf import settings
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from users.views import Index, About
from products.views import Fake

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index, name="index"),
    path('about_us', About, name="about"),
    path('Fake', Fake, name="fake"),
    path('register/', RegisterView.as_view(), name=('register')),
    path('activate/<code>', activate_user_view, name='activate'),
    path('product/', include('products.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

