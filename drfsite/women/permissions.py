from rest_framework import permissions


# ---23.12.2023---
# Lesson 10
# Создадим пользовательский класс разрешений такой, что удалить запись сможет
# только администратор, а просматривать смогут все пользователи
# Все permissions образуются от базового класса BasePermission,
# в котором определены два метода:
# Первый метод has_permission позволяет настраивать права доступа
# на уровне всего запроса (от клиента), а второй метод has_object_permission – права
# доступа на уровне отдельного объекта (данных, записи БД)
class IsAdminOrReadOnly(permissions.BasePermission):
    # Будем управлять правами на уровне всего запроса (True - права предоставлены, False - не предоставлены)
    def has_permission(self, request, view):
        # Если HTTP-запрос - безопасный (только для чтения данных), то предоставляем права доступа для всех
        if request.method in permissions.SAFE_METHODS:
            return True

        # А для всех остальных действий предоставляем доступ только администраторам
        return bool(request.user and request.user.is_staff)


# Класс, предоставляющий права на чтение всем пользователям, а изменение - автору записи (из документации)
class IsOwnerOrReadOnly(permissions.BasePermission):
    # Разрешение предоставляем на уровне объекта (записи), поэтому используем метод has_object_permission
    def has_object_permission(self, request, view, obj):
        # Для безопасных методов даём доступ всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True

        # Если пользователь, указанный в БД, совпадает с пользователем,
        # от которого пришёл запрос, то даём доступ
        return obj.user == request.user
