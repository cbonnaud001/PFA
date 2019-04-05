"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from . import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('valider/', views.get_model),
    path('get_file/', views.search_graph),
    path('get_img/', views.get_img),
    path('get_cl/', views.get_cl),
    path('img_selected/', views.img_selected),
    path('get_filters/', views.get_filters),
    path('reset_nn/', views.reset_nn),
    path('filter_max', views.filter_max),
]
