from django.forms import model_to_dict
from rest_framework import generics
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Women
from .serializers import WomenSerializer


# Create your views here.

"""
# ---13.12.2023---
# Lesson 6
# В Django также существуют предопределённые базовые классы представлений
# для выполнения различных видов запросов:
# CreateAPIView – создание данных по POST-запросу;
# ListAPIView – чтение списка данных по GET-запросу;
# RetrieveAPIView – чтение конкретных данных (записи) по GET-запросу;
# DestroyAPIView – удаление данных (записи) по DELETE-запросу;
# UpdateAPIView – изменение записи по PUT- или PATCH-запросу;
# ListCreateAPIView – для чтения (по GET-запросу) и создания списка данных (по POST-запросу);
# RetrieveUpdateAPIView – чтение и изменение отдельной записи (GET-, PUT- и PATCH-запросы);
# RetrieveDestroyAPIView – чтение (GET-запрос) и удаление (DELETE-запрос) отдельной записи;
# RetrieveUpdateDestroyAPIView – чтение, изменение и добавление отдельной записи (GET-, PUT-, PATCH- и DELETE-запросы)
"""


# ---13.12.2023---
# Lesson 6
# Определим представление на основе ListCreateAPIView, возвращающее список записей по GET-запросу
# и добавляющее новую запись по POST-запросу
# ListCreateAPIView наследуется от следующих классов:
# mixins.ListModelMixin - миксин для определения метода list(),
# mixins.CreateModelMixin - миксин для определения метода create(),
# GenericAPIView - базовый класс для всех APIView
class WomenAPIList(generics.ListCreateAPIView):
    # Список записей, возвращаемых клиенту
    queryset = Women.objects.all()
    # Переопределяем сериализатор
    serializer_class = WomenSerializer


# ---21.12.2023---
# Lesson 7
# Для возможности использования PUT-запроса, который был определён в классе WomenApiView, создадим ещё один класс,
# наследующийся от UpdateAPIView
class WomenAPIUpdate(generics.UpdateAPIView):
    # Т.к. Women.objects.all() является ленивым запросом, то он выполняется не сразу, а просто связывает queryset
    # с моделью, а пользователю возвращается одна конкретная запись
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


# Создадим ещё один класс представления, выполняющий CRUD-операции, на основе класса
# RetrieveUpdateDestroyAPIView
class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


# # ---08.12.2023---
# # Lesson 3
# # Простейший пример работы DRF без сериализатора
# # Создание класса представления DRF на основе APIView (базовый класс представлений)
# # Базовый класс APIView связывает пришедший запрос с соответствующим методом
# class WomenAPIView(APIView):
#     # Метод get отвечает за обработку GET-запросов, request содержит параметры GET-запроса
#     def get(self, request):
#         # Response преобразовывает словарь в json-строку
#         # return Response({'title': 'Angelina Jolie'})
#
#         # Если нужно возвращать данные из БД, то сначала получаем их
#         # Список всех статей из таблицы Women
#         # Ошибка - QuerySet не является JSON-сериализуемым
#         # lst = Women.objects.all()
#         # Должны из QuerySet извлечь values
#         # lst = Women.objects.all().values()
#         # return Response({'posts': list(lst)})
#
#         # ---08.12.2023---
#         # Lesson 4
#         # Получаем QuerySet со всеми статьями
#         w = Women.objects.all()
#         # Параметр many=True говорит сериализатору о том, что будет обрабатываться набор записей
#         # Обращаемся к коллекции data - словарю преобразованных данных из таблицы Women
#         # То, что происходит в методе get - аналог функции encode из serializers.py
#         return Response({'posts': WomenSerializer(w, many=True).data})
#
#     # Если будет отправлен POST-запрос без переопределения метода post, то вернётся json
#     # {
#     #     "detail": "Метод \"POST\" не разрешен."
#     # }
#     # Переопределим POST-запрос так, чтобы он записывал данные в БД
#     def post(self, request):
#         # Выполняем проверку данных из запроса на валидность
#         serializer = WomenSerializer(data=request.data)
#         # Если убрать raise_exception=True, и передать неверные данные, то ошибка будет обработана на уровне Django,
#         # что является не совсем верным, т.к. даже при возникновении ошибок нужно возвращать JSON
#         serializer.is_valid(raise_exception=True)
#         # serializer.is_valid()
#
#         # ---09.12.2023---
#         # Lesson 5
#         # Метод save() сериализатора, если при его создании был передан аргумент data,
#         # вызывает метод create()
#         serializer.save()
#
#         # post_new = Women.objects.create(
#         #     title=request.data['title'],
#         #     content=request.data['content'],
#         #     cat_id=request.data['cat_id']
#         # )
#         # return Response({'title': 'Jennifer Shrader Lawrence'})
#         # Возвращаем созданную запись в json (model_to_dict - функция, преобразующая объект в словарь)
#         # return Response({'post': model_to_dict(post_new)})
#
#         # Используем сериализатор
#         # return Response({'post': WomenSerializer(post_new).data})
#
#         # Можем не создавать объект-сериализатор заново, а обратиться к коллекции data,
#         # которая будет хранить вновь созданный объект, который возвратит метод create
#         return Response({'post': serializer.data})
#
#     # Реализовываем метод put (для PUT-запроса), которому соответствует метод update сериализатора
#     # *args - позиционные аргументы (список)
#     # **kwargs - именованные аргументы (словарь)
#     def put(self, request, *args, **kwargs):
#         # pk - идентификатор записи, которую нужно поменять
#         pk = kwargs.get("pk", None)
#         # Если идентификатор не задан, то выводим ошибку
#         if not pk:
#             return Response({"error": "Method PUT is not allowed"})
#
#         try:
#             instance = Women.objects.get(pk=pk)
#         # Если по такому ключу запись не найдена, выводим ошибку
#         except:
#             return Response({"error": "Object does not exist"})
#
#         # Если был получен ключ и найдена запись, создаём объект-сериализатор
#         # data=request.data - новые данные
#         # instance=instance - запись, которую мы хотим изменить
#         serializer = WomenSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         # Когда создаём сериализатор с параметрами data и instance,
#         # то метод save автоматически вызывает метод update сериализатора
#         serializer.save()
#         return Response({"post": serializer.data})
#
#     # Метод для DELETE-запроса
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE is not allowed"})
#
#         # ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ в Lesson 5
#         # Реализация удаления записи с переданным pk
#         try:
#             instance = Women.objects.get(pk=pk)
#             instance.delete()
#         except:
#             return Response({"error": "Object does not exist"})
#
#         return Response({"post": "delete post " + str(pk)})


# ---06.12.2023---
# Lesson 2
# Создадим представление DRF, которое будет срабатывать на запрос от пользователя
# Класс WomenAPIView наследуется от базового ListAPIView, который берется из DRF и реализует функционал
# по формированию JSON-списка из записей таблицы Women
# Чтобы представление знало как формировать ответ, нужно определить класс сериализатора
# class WomenAPIView(generics.ListAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer
