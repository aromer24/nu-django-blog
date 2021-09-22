from django.db import models
from django.db.models import F
from django.utils.functional import cached_property

from usersapp.models import BlogUser


# 3 типа наследования: abstract, классическое, proxy
class ActiveManager(models.Manager):

    def get_queryset(self):
        all_objects = super().get_queryset()
        return all_objects.filter(is_active=True)


class IsActiveMixin(models.Model):
    objects = models.Manager()
    active_objects = ActiveManager()
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True


class UpdatedObjectsManager(models.Manager):

    def get_queryset(self):
        all_objects = super().get_queryset()
        # Дата обновления не равна дата содания F - запрос
        return all_objects.filter(update=F('create'))


class TimeStamp(models.Model):
    """
    Abstract - для нее не создаются новые таблицы
    данные хранятся в каждом наследнике
    """
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True, db_index=True)

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


class Tag(IsActiveMixin):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


class Post(TimeStamp, IsActiveMixin):
    name = models.CharField(max_length=32, unique=True)
    text = models.TextField()
    # Связь с категорией
    # один - много
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_posts')
    # Связь с тегом
    tags = models.ManyToManyField(Tag)
    # Картинка
    # 2 варианта хранения кратинки (1 - в базе, 2 - на диске)
    image = models.ImageField(upload_to='posts', null=True, blank=True)
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=1)

    @cached_property
    def get_all_tags(self):
        tags = Tag.objects.all()
        return tags

    def has_image(self):
        # print('my image:', self.image)
        # print('type', type(self.image))
        return bool(self.image)

    def some_method(self):
        return 'hello from method'

    def __str__(self):
        return f'{self.name}, category: {self.category.name}'

    def display_tags(self):
        tags = self.tags.all()
        result = ';'.join([item.name for item in tags])
        return result


# Класское наследование
class CoreObject(models.Model):
    name = models.CharField(max_length=32)


class Car(CoreObject):
    # является
    description = models.TextField()


class Toy(CoreObject):
    text = models.TextField()
