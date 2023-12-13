"""
URL configuration for drfsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

# from women.views import WomenAPIView, WomenAPIList
from women.views import *

# ---06.12.2023---
# Lesson 2
# Прописываем маршрут к представлению DRF
# После api/ в URL принято указывать его версию
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/v1/womenlist/', WomenAPIView.as_view()),
    # # ---09.12.2023---
    # # Lesson 5
    # # Дополнительный маршрут для метода put() WomenAPIView,
    # # вызывающего метод update WomenSerializer (передаём ключ pk)
    # path('api/v1/womenlist/<int:pk>/', WomenAPIView.as_view()),
    # ---13.12.2023---
    # Lesson 6
    # Маршруты для WomenAPIList
    path('api/v1/womenlist/', WomenAPIList.as_view()),
    path('api/v1/womenlist/<int:pk>/', WomenAPIList.as_view())
]
