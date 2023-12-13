import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Women


# ---08.12.2023---
# Lesson 4
# Основное предназначение сериализатора - осуществлять конвертацию различных объектов (queryset)
# в формат JSON, и наоборот


# # Определим класс, имитирующий модели фреймворка Django
# class WomenModel:
#     # Инициализатор класса
#     def __init__(self, title, content):
#         # Определяем локальные атрибуты класса
#         self.title = title
#         self.content = content


# # Определяем сериализатор, наследующийся от базового класса Serializer, для которого
# # преобразование данных в JSON и обратно должны будем реализовать самостоятельно
# # Имена переменных в WomenModel и WomenSerializer должны совпадать!!!
# class WomenSerializer(serializers.Serializer):
#     # Напрямую с моделями взаимодействовать нельзя, поэтому нужно определить доп.атрибуты класса сериализатора
#     # serializers.CharField отвечает за представление данных в виде строки
#     # (можем добавить ограничение по длине строки max_length)
#     title = serializers.CharField(max_length=255)
#     # На уровне сериализатора текст и строка - CharField
#     content = serializers.CharField()


# ---09.12.2023---
# Lesson 5
# Обычно в сериализаторе ещё должно выполняться обновление, сохранение и удаление данных,
# а не только преобразование в JSON и обратно
# Ранее этот функционал осуществлялся в классе WomenAPIView
# На практике класс представления отвечает только за обработку запросов,
# а класс сериализатора - за обработку данных
# (в т.ч. за добавление/изменение/чтение записей из БД)


# # Рассмотрим работу сериализатора на примере модели Women из models.py
# class WomenSerializer(serializers.Serializer):
#     # CharField - строковый валидатор сериализатора
#     title = serializers.CharField(max_length=255)
#     content = serializers.CharField()
#     # Поля дат правильнее установить как поля только для чтения (read_only=True)
#     # time_create = serializers.DateTimeField()
#     # time_update = serializers.DateTimeField()
#     time_create = serializers.DateTimeField(read_only=True)
#     time_update = serializers.DateTimeField(read_only=True)
#     is_published = serializers.BooleanField(default=True)
#     # Вместо внешнего ключа в исходной модели в сериализаторе используем целое число
#     cat_id = serializers.IntegerField()
#
#     # Метод, отвечающий за создание записи в БД
#     def create(self, validated_data):
#         # **validated_data - распакованный словарь validated_data
#         return Women.objects.create(**validated_data)
#
#     # Добавим метод, который сможет обновлять существующие данные
#     # instance - ссылка на объект модели Women
#     # validated_data - словарь проверенных данных, которые будем изменять
#     def update(self, instance, validated_data):
#         # Метод get() позволяет взять значение из словаря по ключу,
#         # если не получается взять значение из validated_data, то возвращаем существующее
#         instance.title = validated_data.get("title", instance.title)
#         instance.content = validated_data.get("content", instance.content)
#         # Поле time_update меняем, потому что логично, что при изменении записи оно будет меняться
#         instance.time_update = validated_data.get("time_update", instance.time_update)
#         instance.is_published = validated_data.get("is_published", instance.is_published)
#         instance.cat_id = validated_data.get("cat_id", instance.cat_id)
#         # Сохраняем изменения в записи в БД
#         instance.save()
#         return instance


# ---13.12.2023---
# Lesson 6
# Воспользуемся классом ModelSerializer, упрощающем текст программы при описании сериализаторов,
# связанных с моделями Django
class WomenSerializer(serializers.ModelSerializer):
    # Вложенный класс, определяющий модель, с которой работаем
    class Meta:
        model = Women
        # Указываем возвращаемые пользователю поля
        # (для внешнего ключа прописываем просто cat, а не cat_id)
        # По GET-запросу возвращаются эти 3 поля
        # fields = ("title", "content", "cat")
        # В этом случае возвращаются все поля
        fields = "__all__"


# # Функция для преобразования WomenModel в JSON-формат
# def encode():
#     model = WomenModel('Angelina Jolie', 'Content: Angelina Jolie')
#     # model_sr - объект сериализации
#     model_sr = WomenSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     # Переводим объект сериализации в байтовую строку JSON с помощью JSONRenderer
#     json = JSONRenderer().render(model_sr.data)
#     print(json)


"""
---08.12.2023---
Lesson 4
python manage.py shell
from women.serializers import encode
encode()

{'title': 'Angelina Jolie', 'content': 'Content: Angelina Jolie'}
<class 'rest_framework.utils.serializer_helpers.ReturnDict'>
b'{"title":"Angelina Jolie","content":"Content: Angelina Jolie"}'

quit()
"""


# # Функция для перевода JSON-строки в объект
# def decode():
#     # Имитируем чтение байтовой JSON-строки, поступившей в запросе от клиента
#     stream = io.BytesIO(b'{"title":"Angelina Jolie","content":"Content: Angelina Jolie"}')
#     # JSONParser().parse получает данные из JSON-строки
#     data = JSONParser().parse(stream)
#     # Используем именованный параметр data в сериализаторе, когда декодируем данные
#     serializer = WomenSerializer(data=data)
#     # Осуществляем валидацию данных
#     serializer.is_valid()
#     # Выводим на печать проверенные данные
#     # Получаем упорядоченный словарь, данные из которого можем использовать для создания объекта WomenModel
#     print(serializer.validated_data)


"""
---08.12.2023---
Lesson 4
python manage.py shell
from women.serializers import decode
decode()

OrderedDict([('title', 'Angelina Jolie'), ('content', 'Content: Angelina Jolie')])

quit()
"""


# # ---06.12.2023---
# # Lesson 2
# # Файл для определения классов-сериализаторов
# # Будем использовать класс ModelSerializer, предназначенный для работы с моделями
# class WomenSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Women
#         fields = ('title', 'cat_id')
