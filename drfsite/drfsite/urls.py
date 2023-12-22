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
from django.urls import path, include

# from women.views import WomenAPIView, WomenAPIList
from women.views import *
# # ---21.12.2023---
# # Lesson 8
# # Для маршрутизации при использовании ViewSet можно использовать роутер
# from rest_framework import routers
#
#
# # ---22.12.2023---
# # Lesson 9
# # Иногда может понадобиться создать собственный класс роутера (custom router)
# # Пример из документации по DRF
# class MyCustomRouter(routers.SimpleRouter):
#     # Список из объектов класса Route (маршрутов)
#     routes = [
#         # url - шаблон маршрута (могут быть использованы регулярные выражения)
#         # URL-адреса определены без обратного слэша
#         # mapping - связывает тип HTTP-запроса с соответствующим методом viewset
#         # name - определяет название маршрута
#         # detail - список или отдельная запись
#         # initkwargs – дополнительные аргументы для коллекции kwargs, которые передаются
#         # конкретному представлению при срабатывании маршрута
#         # Маршрут, позволяющий читать список статей
#         routers.Route(url=r'^{prefix}$',
#                       mapping={'get': 'list'},
#                       name='{basename}-list',
#                       detail=False,
#                       initkwargs={'suffix': 'List'}),
#         # Маршрут, позволяющий получить конкретную статью по идентификатору
#         routers.Route(url=r'^{prefix}/{lookup}$',
#                       mapping={'get': 'retrieve'},
#                       name='{basename}-detail',
#                       detail=True,
#                       initkwargs={'suffix': 'Detail'})
#     ]
#
#
# # роутер SimpleRouter формирует два типа маршрутов:
# # http://127.0.0.1:8000/api/v1/women/ - для извлечения списка записей (GET, POST);
# # http://127.0.0.1:8000/api/v1/women/pk/ - для работы с конкретной записью (GET, PUT, DELETE).
# # ---22.12.2023---
# # Lesson 9
# # Вместо SimpleRouter попробуем использовать DefaultRouter
# # router = routers.SimpleRouter()
# # Вместо DefaultRouter попробуем кастомный роутер MyCustomRouter
# # router = routers.DefaultRouter()
# router = MyCustomRouter()
# # Регистрируем маршрут в роутере
# # router.register(r'women', WomenViewSet)
# # Если убрали атрибут queryset из viewset, то нужно указать basename
# router.register(r'women', WomenViewSet, basename='women')
# # router.register(r'women2', WomenViewSet)
# # Префикс в названиях (name) маршрутов в роутере берётся по имени модели (из queryset)
# # Чтобы изменить это поведение по умолчанию, можно прописать атрибут basename
# # (обязательный параметр, если во viewset не указан атрибут queryset)
# # router.register(r'women', WomenViewSet, basename='men')
# print(router.urls)

"""
Для DefaultRouter видим следующие маршруты:
[<URLPattern '^women/$' [name='women-list']>,
 <URLPattern '^women\.(?P<format>[a-z0-9]+)/?$' [name='women-list']>,
 <URLPattern '^women/(?P<pk>[^/.]+)/$' [name='women-detail']>,
 <URLPattern '^women/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='
women-detail']>,
 <URLPattern '^$' [name='api-root']>,
 <URLPattern '^\.(?P<format>[a-z0-9]+)/?$' [name='api-root']>
]

Здесь три группы маршрутов:
/api/v1/women/  (просмотр списка статей и добавление новой статьи)
/api/v1/women/pk/   (получение, изменение и удаление конкретной статьи)
/api/v1/ (возвращает список маршрутов, присутствующих в роутере) (только для DefaultRouter)
"""

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
    # # ---13.12.2023---
    # # Lesson 6
    # # Маршруты для WomenAPIList
    # path('api/v1/womenlist/', WomenAPIList.as_view()),
    # # path('api/v1/womenlist/<int:pk>/', WomenAPIList.as_view())
    # # ---21.12.2023---
    # # Lesson 7
    # # Добавляем маршрут для WomenAPIUpdate
    # path('api/v1/womenlist/<int:pk>/', WomenAPIUpdate.as_view()),
    # # Добавляем маршрут для WomenAPIDetailView
    # path('api/v1/womendetail/<int:pk>/', WomenAPIDetailView.as_view()),
    # # ---21.12.2023---
    # # Lesson 8
    # # Добавляем маршруты для ViewSet привычным нам способом
    # # Для ViewSet в функцию as_view() можно дополнительно передавать
    # # словарь вида HTTP-запрос - вызываемый во ViewSet метод
    # path('api/v1/womenlist/', WomenViewSet.as_view({'get': 'list'})),
    # path('api/v1/womenlist/<int:pk>/', WomenViewSet.as_view({'put': 'update'})),
    # Связываем маршруты роутера с сайтом (генерируется коллекция router.urls)
    # path('api/v1/', include(router.urls)),   # http://127.0.0.1:8000/api/v1/women/

    # ---23.12.2023---
    # Lesson 10
    # Т.к. вернули несколько классов представлений, то в коллекции urlpatterns нужно прописать маршруты к ним
    # Теперь любой пользователь может изменять данные на сайте, а это - чрезмерный риск,
    # поэтому нужно использовать ограничение доступа
    # Базовые варианты permissions в DRF:
    # AllowAny – полный доступ;
    # IsAuthenticated – только для авторизованных пользователей;
    # IsAdminUser – только для администраторов;
    # IsAuthenticatedOrReadOnly – только для авторизованных или всем, но для чтения.
    path('api/v1/women/', WomenAPIList.as_view()),
    path('api/v1/women/<int:pk>/', WomenAPIUpdate.as_view()),
    path('api/v1/womendelete/<int:pk>/', WomenAPIDestroy.as_view()),
]
