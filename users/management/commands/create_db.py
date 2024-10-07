from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Create the database'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE DjangoProject;")
        self.stdout.write(self.style.SUCCESS('Database created successfully'))