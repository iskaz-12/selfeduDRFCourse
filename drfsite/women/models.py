from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# ---06.12.2023---
# Lesson 2
# Создаём модели статей об известных женщинах и категорий статей
class Women(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    # ---23.12.2023---
    # Lesson 10
    # Для изучения ограничений доступа (permissions) в DRF внесём изменения в модель Women
    # Добавим поле user - идентификатор пользователя, добавившего запись
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name