from django.contrib.auth import logout
from django.forms import model_to_dict
from rest_framework import generics, viewsets, mixins
from django.shortcuts import render, redirect
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Women, Category
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
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


# ---21.12.2023---
# Lesson 8
# Для того, чтобы избавиться от избыточности кода в классах представлений, можно воспользоваться классом ViewSet
# class WomenViewSet(viewsets.ModelViewSet):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer


# Если поменять базовый класс ModelViewSet на ReadOnlyModelViewSet,
# то изменится функциональность представления (сможем только читать записи, но не менять их)
# class WomenViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer


# ---27.12.2023---
# Lesson 15
# Можно создавать пользовательские классы пагинации для отдельных API-запросов
# PageNumberPagination - базовый класс для пагинации в DRF (по номерам страниц)
class WomenAPIListPagination(PageNumberPagination):
    # Количество записей на странице
    page_size = 3
    # Определяем название параметра в запросе для указания количества записей на странице
    page_size_query_param = 'page_size'
    # Максимальное значение параметра page_size в запросе
    # max_page_size = 10000
    max_page_size = 2


# ---23.12.2023---
# Lesson 10
# Для изучения работы с правами доступа создадим несколько классов представлений вместо viewset
# Класс, возвращающий список статей
class WomenAPIList(generics.ListCreateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    # Пусть добавлять новые записи смогут только авторизованные пользователи
    # Если убрать определение permission_classes, то будут применяться глобальные настройки доступа
    permission_classes = (IsAuthenticatedOrReadOnly, )
    # ---27.12.2023---
    # Lesson 15
    # Подключаем пользовательский класс пагинации к представлению
    pagination_class = WomenAPIListPagination


# ---23.12.2023---
# Lesson 11
# ДОПОЛНИТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ logout (ДЛЯ ИСПРАВЛЕНИЯ ОШИБКИ 405)
def logout_user(request):
    logout(request)
    # redirect - перенаправление по маршруту
    return redirect('/')


# Класс, меняющий определённую запись
class WomenAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    # Разрешим менять запись только автору, а просматривать - всем пользователям
    # (для этого также нужно будет создать пользовательский класс разрешений)
    # permission_classes = (IsOwnerOrReadOnly, )

    # ---25.12.2023---
    # Lesson 12
    # Поменяем разрешения так, что на страницу детального просмотра
    # могут заходить только авторизованные пользователи
    permission_classes = (IsAuthenticated, )
    # На текущий момент пользователям доступно 2 вида аутентификации:
    # по токенам и по сессиям, но можно конкретизировать вид аутентификации
    # на уровне отдельного представления с помощью атрибута authentication_classes
    # Пусть в данном классе можем получить доступ только по токенам
    # authentication_classes = (TokenAuthentication, )


# Класс, удаляющий определённую запись
class WomenAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    # Предположим, что записи может удалять только администратор
    # permission_classes = (IsAdminUser, )
    # Создали пользовательский класс разрешений
    permission_classes = (IsAdminOrReadOnly,)


# # Можно импортировать все миксины, указанные в ModelViewSet - всё будет работать так же
# # Если удалить какой-то из миксинов, то будет удалена реализуемая этим миксином функциональность
# class WomenViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    # mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    GenericViewSet):
#     # queryset = Women.objects.all()
#     serializer_class = WomenSerializer
#
#     # ---22.12.2023---
#     # Lesson 9
#     # Если нам нужно возвратить не все записи, а только соответствующие каким-либо условиям,
#     # то нужно переопределить метод get_queryset
#     # При переопределении метода get_queryset можно убрать параметр queryset,
#     # НО тогда обязательно нужно прописать параметр basename в router.register
#     def get_queryset(self):
#         # Если хотим получить конкретную запись по pk, нужно определить параметр pk
#         pk = self.kwargs.get("pk")
#
#         if not pk:
#             # Возвращаем первые 3 записи (если pk не задан)
#             return Women.objects.all()[:3]
#
#         # Используем именно метод filter, т.к. метод get_queryset должен возвращать список
#         return Women.objects.filter(pk=pk)
#
#     # Для дополнительных маршрутов можно использовать декоратор @action в классе viewset
#     # Пусть мы хотим вывести список категорий
#     # methods - список разрешённых методов, detail=False - ожидается работа со списком
#     # и маршрут не будет использовать параметр pk
#     # Сам метод уже придумываем самостоятельно
#     # В списке маршрутов появился новый - /women/category/
#     # Если нам нужно получить конкретную категорию по маршруту вида: /women/1/category/,
#     # то нужно прописать detail=True
#     # @action(methods=['get'], detail=False)
#     @action(methods=['get'], detail=True)
#     # Нужно дополнительно определить параметр pk, чтобы избежать ошибки
#     # def category(self, request):
#     def category(self, request, pk=None):
#         # cats = Category.objects.all()
#         # Если хотим возвратить категорию по pk
#         cats = Category.objects.get(pk=pk)
#         # return Response({'cats': [c.name for c in cats]})
#         return Response({'cats': cats.name})


# # ---13.12.2023---
# # Lesson 6
# # Определим представление на основе ListCreateAPIView, возвращающее список записей по GET-запросу
# # и добавляющее новую запись по POST-запросу
# # ListCreateAPIView наследуется от следующих классов:
# # mixins.ListModelMixin - миксин для определения метода list(),
# # mixins.CreateModelMixin - миксин для определения метода create(),
# # GenericAPIView - базовый класс для всех APIView
# class WomenAPIList(generics.ListCreateAPIView):
#     # Список записей, возвращаемых клиенту
#     queryset = Women.objects.all()
#     # Переопределяем сериализатор
#     serializer_class = WomenSerializer
#
#
# # ---21.12.2023---
# # Lesson 7
# # Для возможности использования PUT-запроса, который был определён в классе WomenApiView, создадим ещё один класс,
# # наследующийся от UpdateAPIView
# class WomenAPIUpdate(generics.UpdateAPIView):
#     # Т.к. Women.objects.all() является ленивым запросом, то он выполняется не сразу, а просто связывает queryset
#     # с моделью, а пользователю возвращается одна конкретная запись
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer
#
#
# # Создадим ещё один класс представления, выполняющий CRUD-операции, на основе класса
# # RetrieveUpdateDestroyAPIView
# class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer


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
