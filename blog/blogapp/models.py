from django.db import models
from usersapp.models import BlogUser


# 3 типа наследования: abstract, классическое, proxy


class TimeStamp(models.Model):
    """
    Abstract - для нее не создаются новые таблицы
    данные хранятся в каждом наследнике
    """
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class Category(TimeStamp):
    # Id не надо, он уже сам появиться
    name = models.CharField(max_length=16, unique=True, verbose_name='Name')
    description = models.TextField(blank=True, verbose_name='Desc')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    # Основные типы полей
    # дата
    # models.DateField
    # models.DateTimeField
    # models.TimeField
    # # Числа
    # models.IntegerField
    # models.PositiveIntegerField
    # models.PositiveSmallIntegerField
    # models.FloatField
    # models.DecimalField
    # # Логический
    # models.BooleanField
    # # Байты (blob)
    # models.BinaryField
    # # Картинка
    # models.ImageField
    # # Файл
    # models.FileField
    # # url, email
    # models.URLField
    # models.EmailField

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


class Post(TimeStamp):
    name = models.CharField(max_length=32, unique=True)
    text = models.TextField()
    # Связь с категорией
    # один - много
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Связь с тегом
    tags = models.ManyToManyField(Tag)
    # Картинка
    # 2 варианта хранения кратинки (1 - в базе, 2 - на диске)
    image = models.ImageField(upload_to='posts', null=True, blank=True)
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)

    def has_image(self):
        # print('my image:', self.image)
        # print('type', type(self.image))
        return bool(self.image)

    def some_method(self):
        return 'hello from method'

    def __str__(self):
        return f'{self.name}, category: {self.category.name}'


# Класское наследование
class CoreObject(models.Model):
    name = models.CharField(max_length=32)


class Car(CoreObject):
    # является
    description = models.TextField()


class Toy(CoreObject):
    text = models.TextField()
