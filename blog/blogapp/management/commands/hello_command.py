from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        # path = os.path.join(settings.BASE_DIR, 'blogapp', 'management', 'my.json')
        # with open(path, 'w') as f:
        #     pass
        # Выбираем ВСЕ категории
        print('Привет')
