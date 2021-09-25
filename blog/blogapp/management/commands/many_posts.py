from django.core.management.base import BaseCommand
from mixer.backend.django import mixer

from blogapp.models import Post, Tag, Category
from usersapp.models import BlogUser


# from blogapp.models import Poll

class Command(BaseCommand):

    def handle(self, *args, **options):
        Post.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        BlogUser.objects.filter(is_superuser=False).delete()

        count = 500
        for i in range(count):
            p = (i/count)*100
            print(f'{i}) {p} %')
            mixer.blend(Post)

        print('end')
